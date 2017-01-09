# Assign3

## Dockerised Applications:
* app1: with db instances db1 and db2
* app2: with db instances db3 and db4
* app3: with db instances db5 and db6

## Proxy.py
* Finds the shard key depending on the id from the client and forwards to the required app-db pair, runs on localhost:5005
* Run python proxy.py

## chash.py
* Consistent hashing class, imported in proxy to find the shard key

## mysql container
* Run docker run -d -p 3306:3306 --name mysqlserver -e MYSQL_ROOT_PASSWORD=password mysql
* To access mysql: docker exec -it mysqlserver mysql -uroot -ppassword

## App1 docker running on 192.168.99.100:5000
* cd app1
* docker build -t app1:latest .
* docker run -p 5000:5000 --name a1 --link mysqlserver:mysql -d app1

## App2 docker running on 192.168.99.100:5001
* cd app2
* docker build -t app2:latest .
* docker run -p 5001:5001 --name a2 --link mysqlserver:mysql -d app2


## App3 docker running on 192.168.99.100:5002
* cd app3
* docker build -t app3:latest .
* docker run -p 5002:5002 --name a3 --link mysqlserver:mysql -d app3

------------------------------------------------------------------------------------------------------

## Input #1
```json
{
    "id" : "1",
    "name" : "Foo 1",
    "email" : "foo1@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "700",
    "submit_date" : "12-10-2016"
}
```
### GET of id: 1
{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 1", 
"decision_date": "", "submit_date": "12-10-2016", "description": "iPad for office use", "id": "1", "estimated_costs": "700", "email": "Foo 1"}

------------------------------------------------------------------------------------------------------

## Input #2
```json
{
    "id" : "2",
    "name" : "Foo 2",
    "email" : "foo2@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "800",
    "submit_date" : "12-10-2016"
}
```

### GET of id: 2

{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 2", "decision_date": "", 
"submit_date": "12-10-2016", "description": "iPad for office use", "id": "2", "estimated_costs": "800", "email": "Foo 2"}

------------------------------------------------------------------------------------------------------

## Input #3
```json
{
    "id" : "3",
    "name" : "Foo 3",
    "email" : "foo3@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "600",
    "submit_date" : "12-10-2016"
}
```

### GET of id: 3
{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 3", "decision_date": "", 
"submit_date": "12-10-2016", "description": "iPad for office use", "id": "3", "estimated_costs": "600", "email": "Foo 3"}

-------------------------------------------------------------------------------------------------------

## Input #4
```json
{
    "id" : "4",
    "name" : "Foo 4",
    "email" : "foo4@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "900",
    "submit_date" : "12-10-2016"
}
```

### GET of id: 4

{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 4", "decision_date": "", 
"submit_date": "12-10-2016", "description": "iPad for office use", "id": "4", "estimated_costs": "900", "email": "Foo 4"}

-----------------------------------------------------------------------------------------------------------

##  Input  #5
```json
{
    "id" : "5",
    "name" : "Foo 5",
    "email" : "foo5@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "700",
    "submit_date" : "12-10-2016"
}
```

### GET of id: 5 

{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 5", "decision_date": "", 
"submit_date": "12-10-2016", "description": "iPad for office use", "id": "5", "estimated_costs": "700", "email": "Foo 5"}

--------------------------------------------------------------------------------------------------------------

##  Input  #6 
```json
{
    "id" : "6",
    "name" : "Foo 6",
    "email" : "foo5@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "800",
    "submit_date" : "12-10-2016"
}
```

### GET of id: 6 

{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 6", 
"decision_date": "", "submit_date": "12-10-2016", "description": "iPad for office use", "id": "6", "estimated_costs": "800", "email": "Foo 6"}

-------------------------------------------------------------------------------------------------------------------------

##  Input  #7 
```json
{
    "id" : "7",
    "name" : "Foo 7",
    "email" : "foo5@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "500",
    "submit_date" : "12-10-2016"
}
```

### GET of id: 7 

{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 7", "decision_date": "", 
"submit_date": "12-10-2016", "description": "iPad for office use", "id": "7", "estimated_costs": "500", "email": "Foo 7"}

------------------------------------------------------------------------------------------------------------------------------

##  Input  #8
```json
{
    "id" : "8",
    "name" : "Foo 8",
    "email" : "foo5@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "600",
    "submit_date" : "12-10-2016"
}
```

### GET of id: 8 

{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 8", "decision_date": "", 
"submit_date": "12-10-2016", "description": "iPad for office use", "id": "8", "estimated_costs": "600", "email": "Foo 8"}

-------------------------------------------------------------------------------------------------------------------------------

##  Input  #9 
```json
{
    "id" : "9",
    "name" : "Foo 9",
    "email" : "foo5@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "700",
    "submit_date" : "12-10-2016"
}
```

### GET of id: 9 

{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 9", "decision_date": "", 
"submit_date": "12-10-2016", "description": "iPad for office use", "id": "9", "estimated_costs": "700", "email": "Foo 9"}

---------------------------------------------------------------------------------------------------------------

##  Input  #10
```json
{
    "id" : "10",
    "name" : "Foo 10",
    "email" : "foo10@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "800",
    "submit_date" : "12-10-2016"
}
```

### GET of id: 10 

{"category": "office supplies", "status": "Pending", "link": "http://www.apple.com/shop/buy-ipad/ipad-pro", "name": "Foo 10", "decision_date": "", 
"submit_date": "12-10-2016", "description": "iPad for office use", "id": "10", "estimated_costs": "800", "email": "Foo 10"}

------------------------------------------------------------------------------------------------------------------------------------------


## Logs 
Also attached as expense.log with all the post and get requests

* INFO:werkzeug: * Restarting with stat
* WARNING:werkzeug: * Debugger is active!
* INFO:werkzeug: * Debugger pin code: 212-758-991
* INFO:werkzeug: * Running on http://0.0.0.0:5005/ (Press CTRL+C to quit)
* INFO:Proxy:Fetching http://192.168.99.100:5001/v1/expenses
* INFO:Proxy:got shard id as 4
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:16:24] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:Proxy:Fetching http://192.168.99.100:5001/v1/expenses
* INFO:Proxy:got shard id as 4
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:17:25] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:Proxy:Fetching http://192.168.99.100:5000/v1/expenses
* INFO:Proxy:got shard id as 2
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:17:42] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:Proxy:Fetching http://192.168.99.100:5001/v1/expenses
* INFO:Proxy:got shard id as 4
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:18:01] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:Proxy:Fetching http://192.168.99.100:5000/v1/expenses
* INFO:Proxy:got shard id as 2
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:18:17] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:Proxy:Fetching http://192.168.99.100:5000/v1/expenses
* INFO:Proxy:got shard id as 2
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:18:32] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:Proxy:Fetching http://192.168.99.100:5001/v1/expenses
* INFO:Proxy:got shard id as 4
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:18:45] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:Proxy:Fetching http://192.168.99.100:5001/v1/expenses
* INFO:Proxy:got shard id as 4
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:18:57] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:Proxy:Fetching http://192.168.99.100:5001/v1/expenses
* INFO:Proxy:got shard id as 3
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:19:09] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:Proxy:Fetching http://192.168.99.100:5000/v1/expenses
* INFO:Proxy:got shard id as 2
* INFO:Proxy:Response 201
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:19:21] "POST /v1/expenses HTTP/1.1" 201 -
* INFO:werkzeug: * Detected change in 'C:\\Users\\DuKE\\Documents\\anubha_sjsu\\cmpe273\\cmpe273_A3\\proxy.py', reloading
* INFO:werkzeug: * Restarting with stat
* WARNING:werkzeug: * Debugger is active!
* INFO:werkzeug: * Debugger pin code: 212-758-991
* INFO:werkzeug: * Running on http://0.0.0.0:5005/ (Press CTRL+C to quit)
* INFO:Proxy:Processing GET on http://192.168.99.100:5001/v1/expenses/1/4
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:20:54] "GET /v1/expenses/1 HTTP/1.1" 200 -
* INFO:Proxy:Processing GET on http://192.168.99.100:5001/v1/expenses/2/4
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:21:46] "GET /v1/expenses/2 HTTP/1.1" 200 -
* INFO:Proxy:Processing GET on http://192.168.99.100:5000/v1/expenses/3/2
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:22:21] "GET /v1/expenses/3 HTTP/1.1" 200 -
* INFO:Proxy:Processing GET on http://192.168.99.100:5001/v1/expenses/4/4
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:22:38] "GET /v1/expenses/4 HTTP/1.1" 200 -
* INFO:Proxy:Processing GET on http://192.168.99.100:5000/v1/expenses/5/2
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:23:12] "GET /v1/expenses/5 HTTP/1.1" 200 -
* INFO:Proxy:Processing GET on http://192.168.99.100:5000/v1/expenses/6/2
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:23:53] "GET /v1/expenses/6 HTTP/1.1" 200 -
* INFO:Proxy:Processing GET on http://192.168.99.100:5001/v1/expenses/7/4
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:24:16] "GET /v1/expenses/7 HTTP/1.1" 200 -
* INFO:Proxy:Processing GET on http://192.168.99.100:5001/v1/expenses/8/4
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:24:32] "GET /v1/expenses/8 HTTP/1.1" 200 -
* INFO:Proxy:Processing GET on http://192.168.99.100:5001/v1/expenses/9/3
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:24:52] "GET /v1/expenses/9 HTTP/1.1" 200 -
* INFO:Proxy:Processing GET on http://192.168.99.100:5000/v1/expenses/10/2
* INFO:Proxy:Response 200
* INFO:werkzeug:127.0.0.1 - - [13/Dec/2016 02:25:10] "GET /v1/expenses/10 HTTP/1.1" 200 -