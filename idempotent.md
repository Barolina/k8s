#### Definition

- namespaces = default
- ingress = True
- generate uuid  and  save uuid in bd,  in header for idempotent
- попыталась  съимитировать, идемпотентность дубликатом  запроса в  постмане )

#### Install

```
> minikube enable ingress
> kubectl apply -f app-orders.yaml
> helm install larisa ./hello-chart
> newman run -n 2 "order idempotent.postman_collection.json"
```

#### Test

```
order idempotent

Iteration 1/2

→ получить  список товаров
  GET http://arch.homework/things [200 OK, 320B, 89ms]
  ✓  [INFO] Request: [object Object]
  ✓  [INFO] Response: [{"id": 1, "name": "th_1", "price": 2}, {"id": 2, "name": "th_3", "price": 4}, {"id": 3, "name": "th_5", "price": 6}, {"id": 4, "name": "th_6", "price": 8}]

→ получить  инфу  о товаре
  GET http://arch.homework/things/2 [200 OK, 247B, 39ms]
  ✓  [INFO] Request: [object Object]
  ✓  [INFO] Response: {
  "id": 2, 
  "name": "th_3", 
  "price": 4
}


→ купить  товар
  POST http://arch.homework/buy/things [200 OK, 176B, 23ms]
  ✓  [INFO] Request: {"id": 2}
  ✓  [INFO] Response: {
  "status": "ok"
}

  ✓  test token data

→ купить  товар  дубликат
  POST http://arch.homework/buy/things [429 TOO MANY REQUESTS, 320B, 16ms]
  ✓  [INFO] Request: {"id": 2}
  ✓  [INFO] Response: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>429 Too Many Requests</title>
<h1>Too Many Requests</h1>
<p>if you buy it</p>

  ✓  test token data

Iteration 2/2

→ получить  список товаров
  GET http://arch.homework/things [200 OK, 320B, 11ms]
  ✓  [INFO] Request: [object Object]
  ✓  [INFO] Response: [{"id": 1, "name": "th_1", "price": 2}, {"id": 2, "name": "th_3", "price": 4}, {"id": 3, "name": "th_5", "price": 6}, {"id": 4, "name": "th_6", "price": 8}]

→ получить  инфу  о товаре
  GET http://arch.homework/things/2 [200 OK, 247B, 37ms]
  ✓  [INFO] Request: [object Object]
  ✓  [INFO] Response: {
  "id": 2, 
  "name": "th_3", 
  "price": 4
}


→ купить  товар
  POST http://arch.homework/buy/things [200 OK, 176B, 19ms]
  ✓  [INFO] Request: {"id": 2}
  ✓  [INFO] Response: {
  "status": "ok"
}

  ✓  test token data

→ купить  товар  дубликат
  POST http://arch.homework/buy/things [429 TOO MANY REQUESTS, 320B, 15ms]
  ✓  [INFO] Request: {"id": 2}
  ✓  [INFO] Response: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>429 Too Many Requests</title>
<h1>Too Many Requests</h1>
<p>if you buy it</p>

  ✓  test token data

┌─────────────────────────┬───────────────────┬──────────────────┐
│                         │          executed │           failed │
├─────────────────────────┼───────────────────┼──────────────────┤
│              iterations │                 2 │                0 │
├─────────────────────────┼───────────────────┼──────────────────┤
│                requests │                 8 │                0 │
├─────────────────────────┼───────────────────┼──────────────────┤
│            test-scripts │                14 │                0 │
├─────────────────────────┼───────────────────┼──────────────────┤
│      prerequest-scripts │                12 │                0 │
├─────────────────────────┼───────────────────┼──────────────────┤
│              assertions │                20 │                0 │
├─────────────────────────┴───────────────────┴──────────────────┤
│ total run duration: 768ms                                      │
├────────────────────────────────────────────────────────────────┤
│ total data received: 732B (approx)                             │
├────────────────────────────────────────────────────────────────┤
│ average response time: 31ms [min: 11ms, max: 89ms, s.d.: 23ms] │
└────────────────────────────────────────────────────────────────┘
```
