import os
import json

from flask import Flask, redirect, url_for, request

app = Flask(__name__)

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ['HOSTNAME'],
    'GREETING': os.environ.get('GREETING', 'Hello'),
}

from sqlalchemy import create_engine

@app.route("/")
def hello():
    return config['GREETING'] + ' from ' + config['HOSTNAME'] + '!'

@app.route("/config")
def configuration():
    return json.dumps(config)


@app.route("/version")
def version():
    return {"version": "skaffold"}

@app.route('/users')
def db():

    engine = create_engine(config['DATABASE_URI'], echo=True)
    
    with engine.connect() as connection:
        result = connection.execute("select id, name from client;")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

@app.route('/adduser', methods=['POST'])
def post_client():
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO client (name)
             VALUES("""
    conn = None
    vendor_id = None
    engine = create_engine(config['DATABASE_URI'], echo=True)
    with engine.connect() as connection: 
      connection.execute("insert into client (name) values ('" +request.form['name']+"');")
    return json.dumps({"status": "ok"})

@app.route('/users/<user_id>', methods=['DELETE'])
def del_client(user_id):
    """ insert a new vendor into the vendors table """
    sql = """delete from client
             where id="""
    conn = None
    vendor_id = None
    engine = create_engine(config['DATABASE_URI'], echo=True)
    print(user_id)
    with engine.connect() as connection: 
      connection.execute(sql +user_id+";")
    return json.dumps({"status": "ok"})

@app.route('/users/<user_id>', methods=['PUT'])
def update_client(user_id):
    """ insert a new vendor into the vendors table """
    sql = """update client set name=
             where id="""
    conn = None
    vendor_id = None
    engine = create_engine(config['DATABASE_URI'], echo=True)
    try:
      with engine.connect() as connection: 
        connection.execute("update client set name='"+request.form['name']+"' where id="+user_id+";")
      return json.dumps({"status": "ok"})
    except:
      return json.dumps({"error": "not found user"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
