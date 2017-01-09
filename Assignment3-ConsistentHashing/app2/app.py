from flask import Flask
from flask import request
from model import db
from model import expense_3, expense_4
from model import CreateDB
from model import app #as application
import json
from sqlalchemy.exc import IntegrityError
import os

# initate flask app
#app = Flask(__name__)

@app.route('/')
def index():
#----------creating the database and tables---------------
	return 'Hello! Welcome to App #2'
	#return socket.gethostbyname(socket.gethostname())
#---------------------------------------------------------


#---------POST METHOD-------------------------------------
@app.route('/v1/expenses',methods=['POST'])
def order_insert():

	if request.method == 'POST':
		try:
			val=json.loads(request.data)
		
			shard_key = val['shard_id']
			
			if shard_key % 2 == 1:
				order_i = expense_3(val['id'],
					val['name'],
					val['email'],
					val['category'], 
					val['description'],
					val['link'],
					val['estimated_costs'],
					val['submit_date'],
					"Pending",
					"")
			else:
				order_i = expense_4(val['id'],
					val['name'],
					val['email'],
					val['category'], 
					val['description'],
					val['link'],
					val['estimated_costs'],
					val['submit_date'],
					"Pending",
					"")
			
			db.session.add(order_i)
			db.session.commit()
			order_id=order_i.id
			return json.dumps({'id':order_id,'name':order_i.name,'email':order_i.email,'category':order_i.category,'description':order_i.description,'link':order_i.link,'estimated_costs':order_i.estimated_costs,'submit_date':order_i.submit_date,'status':order_i.status,'decision_date':order_i.decision_date}),201
		except IntegrityError:
			return json.dumps({'status':False})
#--------------------------------------------------------------


#----------GET, PUT, DELETE METHOD-----------------------------
@app.route('/v1/expenses/<order_id>/<shard_id>', methods = ['GET','PUT','DELETE'])

def get_order(order_id, shard_id):

#----------GET
	if request.method == 'GET':
		try:
			if int(shard_id) % 2 == 1:
				order_g = expense_3.query.filter_by(id=order_id).first()
				if order_g is not None:
					return json.dumps({'id':order_id,'name':order_g.name,'email':order_g.name,'category':order_g.category,'description':order_g.description,'link':order_g.link,'estimated_costs':order_g.estimated_costs,'submit_date':order_g.submit_date,'status':order_g.status,'decision_date':order_g.decision_date})
				else:
					return json.dumps({'status':False}),404
			else:
				order_g = expense_4.query.filter_by(id=order_id).first()
				if order_g is not None:
					return json.dumps({'id':order_id,'name':order_g.name,'email':order_g.name,'category':order_g.category,'description':order_g.description,'link':order_g.link,'estimated_costs':order_g.estimated_costs,'submit_date':order_g.submit_date,'status':order_g.status,'decision_date':order_g.decision_date})
				else:
					return json.dumps({'status':False}),404
		except IntegrityError:
			return json.dumps({'status':False})

#---------PUT
	elif request.method == 'PUT':
		try:
			if int(shard_id) % 2 == 1:
				order_p = expense_3.query.filter_by(id=order_id).first()
				if order_p is not None:
					up_val = json.loads(request.data)
					order_p.estimated_costs = up_val['estimated_costs']
					db.session.commit()
					return json.dumps({'id':order_id,'name':order_p.name,'email':order_p.name,'category':order_p.category,'description':order_p.description,'link':order_p.link,'estimated_costs':order_p.estimated_costs,'submit_date':order_p.submit_date,'status':order_p.status,'decision_date':order_p.decision_date}),202
				else:
					return json.dumps({'status':False}),502
			else:
				order_p = expense_4.query.filter_by(id=order_id).first()
				if order_p is not None:
					up_val = json.loads(request.data)
					order_p.estimated_costs = up_val['estimated_costs']
					db.session.commit()
					return json.dumps({'id':order_id,'name':order_p.name,'email':order_p.name,'category':order_p.category,'description':order_p.description,'link':order_p.link,'estimated_costs':order_p.estimated_costs,'submit_date':order_p.submit_date,'status':order_p.status,'decision_date':order_p.decision_date}),202
				else:
					return json.dumps({'status':False}),502
		except IntegrityError:
			return json.dumps({'status':False})
	
#--------DELETE
	elif request.method == 'DELETE':
		try:
			if int(shard_id) % 2 == 1:
				order_d = expense_3.query.filter_by(id=order_id).first()
				if order_d is not None:
					db.session.delete(order_d)
					db.session.commit()
					return json.dumps({'status': True}),204
				else:
					return json.dumps({'staus':False}),404
			else:
				order_d = expense_4.query.filter_by(id=order_id).first()
				if order_d is not None:
					db.session.delete(order_d)
					db.session.commit()
					return json.dumps({'status': True}),204
				else:
					return json.dumps({'staus':False}),404
		except IntegrityError:
			return json.dumps({'status':False})
#-------------------------------------------------------------------------------------


#----run app service---- 
if __name__ == "__main__":
	HOSTNAME = 'mysqlserver'
	database = CreateDB(hostname = HOSTNAME)
	app.run(host='0.0.0.0', port=5001, debug=True)
