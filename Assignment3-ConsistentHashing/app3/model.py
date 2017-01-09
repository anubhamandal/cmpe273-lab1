from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Database Configurations
app = Flask(__name__)
DATABASE1 = 'ExpenseDB_5'
DATABASE2 = 'ExpenseDB_6'
PASSWORD = 'password'
USER = 'root'
HOSTNAME = 'mysqlserver'


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)

databases = {
    'db5': 'mysql://root:password@mysqlserver:3306/ExpenseDB_5',
    'db6': 'mysql://root:password@mysqlserver:3306/ExpenseDB_6'
}

app.config['SQLALCHEMY_BINDS'] = databases

db = SQLAlchemy(app)

#define models including __bind_key__, which should tell SQLAlchemy which DB it needs to use

#---------------------------------------DB1---------------------------------------------------------------------
class expense_5(db.Model):

	__tablename__ = 'expense5'
    	__bind_key__ = 'db5'
	
	# Data Model Order Table
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	email = db.Column(db.String(120))
	category = db.Column(db.String(120))
	description = db.Column(db.String(120))
	link = db.Column(db.String(200))
	estimated_costs = db.Column(db.String(50))
	submit_date = db.Column(db.String(50))
	status = db.Column(db.String(50))
	decision_date = db.Column(db.String(50))

	def __init__(self, id, name, email, category, description, link, estimated_costs, submit_date, status, decision_date):
		# initialize columns
		self.id = id
		self.name = name
		self.email = email
		self.category = category
		self.description = description
		self.link = link
		self.estimated_costs = estimated_costs
		self.submit_date = submit_date
		self.status = status
		self.decision_date = decision_date
		
#---------------------------------------DB2-----------------------------------------------------
class expense_6(db.Model):

	__tablename__ = 'expense6'
    	__bind_key__ = 'db6'
	
	# Data Model Order Table
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	email = db.Column(db.String(120))
	category = db.Column(db.String(120))
	description = db.Column(db.String(120))
	link = db.Column(db.String(200))
	estimated_costs = db.Column(db.String(50))
	submit_date = db.Column(db.String(50))
	status = db.Column(db.String(50))
	decision_date = db.Column(db.String(50))

	def __init__(self, id, name, email, category, description, link, estimated_costs, submit_date, status, decision_date):
		# initialize columns
		self.id = id
		self.name = name
		self.email = email
		self.category = category
		self.description = description
		self.link = link
		self.estimated_costs = estimated_costs
		self.submit_date = submit_date
		self.status = status
		self.decision_date = decision_date

		
#----------------------------------Creating Databases-----------------------------------------		
class CreateDB():
	def __init__(self, hostname=None):
		if hostname != None:	
			HOSTNAME = hostname
		import sqlalchemy
		engine = sqlalchemy.create_engine('mysql://%s:%s@%s'%(USER, PASSWORD, HOSTNAME)) # connect to server
		engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE1)) #create db
		engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE2)) #create db
		#engine.execute("USE ExpenseDB;")
		db.create_all()
		db.session.commit()

if __name__ == '__main__':
	manager.run()
