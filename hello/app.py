import time

import os
import json
import uuid
from flask import Flask, request, abort, redirect

app = Flask(__name__)

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', 'http://172.0.0.2:32000'),
}

from sqlalchemy import create_engine

engine = create_engine(config['DATABASE_URI'], echo=True)

SESSIONS = {}
HASH_BYU = list()


@app.route('/users/me')
def me():
    if not 'X-UserId' in request.headers:
        return "Not authenticated yes"
    data = {}
    data['id'] = request.headers['X-UserId']
    data['login'] = request.headers['X-User']
    data['email'] = request.headers['X-Email']
    data['first_name'] = request.headers['X-First-Name']
    data['last_name'] = request.headers['X-Last-Name']
    return data


@app.route('/buy/things', methods=["POST"])
def buy():
    request_data = request.get_json()
    # add validation
    id_things = request_data['id']
    print(request.headers)
    Etag = None
    try:
        Etag = request.headers['x-api-key']
    except Exception as e:
        print(e)
        abort(400)

    try:
        with engine.connect() as connection:
            result = connection.execute(
                """
                insert into hash_tag (oid)
                values ('{}') returning id;
                """.format(str(Etag))).first()
        return {"status": "ok"}
    except Exception as e:
        print(e)
        abort(429, "if you buy it")



@app.route('/things')
def things():
    rows = []
    with engine.connect() as connection:
        result = connection.execute(
            "select * from things")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)


@app.route('/things/<thing_id>')
def things_id(thing_id):
    engine = create_engine(config['DATABASE_URI'], echo=True)
    with engine.connect() as connection:
        result = connection.execute("select * from things where id =" + thing_id + ";")
        rows = [dict(r.items()) for r in result]
        print(result)
        print("yest  result ")
        response = app.make_response({"id": 1, "price": 2, "name": "th_1"})
        if isinstance(rows, list):
            response = app.make_response(rows[0])
        e_tag = str(uuid.uuid4())
        response.headers['Etag'] = e_tag
    return response


def generate_session_id(size=40):
    import string
    import random
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))


def create_session(data):
    session_id = generate_session_id()
    SESSIONS[session_id] = data
    return session_id


def register_user(login, password, email, first_name='', last_name=''):
    try:
        with engine.connect() as connection:
            result = connection.execute(
                """
                insert into auth_user (login, password, email, first_name, last_name)
                values ('{}', '{}', '{}', '{}', '{}') returning id;
                """.format(login, password, email, first_name, last_name)).first()
            id_ = result['id']
        return {"id": id_}
    except Exception as e:
        print(e)
        abort(400, "login/email already exists")


def get_user_by_credentials(login, password):
    rows = []
    with engine.connect() as connection:
        result = connection.execute(
            "select id, login, email, first_name, last_name from auth_user "
            "where login='{}' and password='{}'".format(login, password))
        rows = [dict(r.items()) for r in result]
    return rows[0]


@app.route("/sessions", methods=["GET"])
def sessions():
    return SESSIONS


@app.route("/register", methods=["POST"])
def register():
    request_data = request.get_json()
    # add validation
    login = request_data['login']
    password = request_data['password']
    email = request_data['email']
    first_name = request_data.get('first_name', '')
    last_name = request_data.get('last_name', '')
    return register_user(login, password, email, first_name, last_name)


@app.route('/update_profile', methods=['PUT'])
def update_client():
    """ update  """
    if not 'X-UserId' in request.headers:
        return "Not authenticated yes"
    request_data = request.get_json()
    data = {}
    data['id'] = request.headers['X-UserId']
    data['login'] = request.headers['X-User']
    data['email'] = request.headers['X-Email']
    data['first_name'] = request_data.get('first_name', request.headers['X-First-Name'])
    data['last_name'] = request_data.get('last_name', request.headers['X-Last-Name'])
    with engine.connect() as connection:
        connection.execute(
            """
            update auth_user set first_name ='{}', last_name ='{}' where id={};
            """.format(data['first_name'], data['last_name'], data['id']))

    try:
        session_id = request.cookies['session_id']
        SESSIONS[session_id] = data
    except Exception as e:
        raise Exception("not session " + e)

    try:
        response = app.make_response(data)
        response.headers['X-UserId'] = data['id']
        response.headers['X-User'] = data['login']
        response.headers['X-Email'] = data['email']
        response.headers['X-First-Name'] = data['first_name']
        response.headers['X-Last-Name'] = data['last_name']
        return response
    except Exception as e:
        raise Exception("error in create header " + e)


@app.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    login = request_data['login']
    password = request_data['password']
    user_info = get_user_by_credentials(login, password)
    if user_info:
        session_id = create_session(user_info)
        response = app.make_response({"status": "ok"})
        response.set_cookie("session_id", session_id, httponly=True)
        return response
    else:
        abort(401)


@app.route("/signin", methods=["GET"])
def signin():
    return {"message": "Please go to login and provide Login/Password"}


@app.route('/auth')
def auth():
    print(request.cookies)
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        if session_id in SESSIONS:
            data = SESSIONS[session_id]
            response = app.make_response(data)
            response.headers['X-UserId'] = data['id']
            response.headers['X-User'] = data['login']
            response.headers['X-Email'] = data['email']
            response.headers['X-First-Name'] = data['first_name']
            response.headers['X-Last-Name'] = data['last_name']
            return response
    abort(401)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    response = app.make_response({"status": "ok"})
    response.set_cookie('session_id', '', expires=0)
    return response


@app.route("/health")
def health():
    return {"status": "OK"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
