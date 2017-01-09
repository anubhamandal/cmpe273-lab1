from flask import Flask
from flask import request, Response
import requests
import logging
import ast
import json
from chash import ConsistentHashRing

"""CONSISTENT HASHING"""
#My app and DB mapping
# mySetup[database id] = [app, db_instance]
mySetup = {}
mySetup[1] = [1,1]  
mySetup[2] = [1,2]
mySetup[3] = [2,1]
mySetup[4] = [2,2]
mySetup[5] = [3,1]
mySetup[6] = [3,2]

# Object created for consistent hashing with 1 replica
ring = ConsistentHashRing(1)

for key, value in mySetup.items():
    ring["app%d:%d" % (value[0],value[1])] = key

"""CONSTANTS"""
app = Flask(__name__)
logging.basicConfig(filename="expense.log", level=logging.INFO)
LOG = logging.getLogger("Proxy")
myhosts = ["http://192.168.99.100:5000","http://192.168.99.100:5001","http:192.168.99.100:5002"]
db_host = {1:myhosts[0], 2:myhosts[0], 3:myhosts[1], 4:myhosts[1], 5:myhosts[2], 6:myhosts[2]}
EXPENSE_API = '/v1/expenses'


"""POST EXPENSE"""

@app.route(EXPENSE_API, methods=['POST'])
def post_expenses():
    def func(count):
        try:
	    x = ast.literal_eval(request.get_data())
	    shard_key = ring[x['id']]
	    print shard_key
	    url = db_host[shard_key] + EXPENSE_API
	    LOG.info("Fetching %s", url)
	    LOG.info("got shard id as %d", shard_key)
	    x['shard_id'] = shard_key
	    y = json.dumps(x)
            r = post_request(url, y)
        except Exception as e:
            return parse_exception(e)
        return parse_response(r)
    retry_count = 0
    return func(retry_count)


"""GET/UPDATE/DELETE EXPENSE"""

@app.route(EXPENSE_API + '/<order_id>', methods=['GET', 'PUT', 'DELETE'])
def get_expenses(order_id):
    def func(count):
        try:
            shard_key = ring[str(order_id)]
            print shard_key
	    url = db_host[shard_key] + EXPENSE_API + '/' + order_id + '/' + str(shard_key)
	    LOG.info("Processing {} on {}".format(request.method, url))
            if request.method == 'GET':
                r = get_request(url)
            elif request.method == 'DELETE':
                r = delete_request(url)
            elif request.method == 'PUT':
                r = update_request(url, request.get_data())
        except Exception as e:
            return parse_exception(e)
        return parse_response(r)
    retry_count = 0
    return func(retry_count)


""" REQUEST APIs """

def post_request(url, json_data, headers=None):
    r = requests.post(url, data=json_data, headers=headers)
    return r

def get_request(url, params=None, headers=None):
    r = requests.get(url, params=params, headers=headers)
    return r

def delete_request(url):
    r = requests.delete(url)
    return r

def update_request(url, json_data):
    r = requests.put(url, data=json_data)
    return r


"""RESPONSE APIs"""

def parse_response(r):
    LOG.info("Response %s", r.status_code)
    resp = Response(r.text, status=r.status_code)
    return resp

def parse_exception(e):
    LOG.error(e.message)
    return Response("Internal Error", status=500)


""" MAIN """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)
