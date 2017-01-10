# encoding: utf8

from flask import Flask
from flaskext.mysql import MySQL
import urllib2, json

mysql = MySQL()
app=Flask(__name__)
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='password'
app.config['MYSQL_DATABASE_DB']='crime'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

from spyne.application import Application
from spyne import ComplexModel, Array
from spyne.decorator import rpc
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Unicode, String, Float
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.service import ServiceBase

class Output(ComplexModel):
		_type_info = {
			'total_crime':Unicode,
			'the_most_dangerous_street':Unicode,
			'crime_type_count':Unicode,
			'event_time_count':Unicode,
		}

class HelloWorldService(ServiceBase):
	@rpc(Unicode,Unicode,Unicode, _returns=Array(Output))
	def checkcrime(ctx, lat, lon, radius):

		#---------------creating table-----------
		cursor = mysql.connect().cursor()
		query="DROP TABLE if exists `crimedb`"
		cursor.execute(query)
		query="CREATE TABLE crimedb (cdid int, type varchar(15), date DATETIME, address varchar(50))"
		cursor.execute(query)
		cursor.close()
		
		#----------inserting in the table--------
		temp_data = json.load(urllib2.urlopen('https://api.spotcrime.com/crimes.json?lat=%r&lon=%r&radius=%r&key=.'%(lat,lon,radius)))
		data = temp_data['crimes']
		no_crimes=len(data)
		for i in range(0,no_crimes):
			crime_cdid=data[i]['cdid']
			crime_type=data[i]['type']
			crime_date=data[i]['date']
			crime_address=data[i]['address']
			cursor = mysql.connect().cursor()
			cursor.execute("Insert into crimedb values (%r,%r,%r,%r)"%(crime_cdid,crime_type,crime_date,crime_address))
			mysql.commit()
			cursor.close()

		#-----Total no of crimes------------------------
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT count(*) from CrimeDB")
		x = cursor.fetchone()
		data1 = x[0]
		cursor.close()

		#-----Top 3 streets-----------------------------
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT g.street from (SELECT distinct f.street,count(*) as count from (SELECT trim(c.str) as street from (SELECT substr(a.addr,1,instr(a.addr,'&')-1) as str from (SELECT substr(d.address,instr(d.address,'of')+3) as addr from crimedb d) a union all SELECT substr(b.addr,instr(b.addr,'&')+2) as str from (SELECT substr(e.address,instr(e.address,'of')+3) as addr from crimedb e) b) c) f group by f.street order by 2 desc) g limit 1,3")
		data2 = cursor.fetchall()
		cursor.close()
		
		#-----Crime type count--------------------------
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT concat(a.type,' : ',a.count) from (select distinct b.type, count(*) as count from CrimeDB b group by type) a")
		data3 = cursor.fetchall()
		cursor.close()
		
		#-----Time range--------------------------------
		cursor = mysql.connect().cursor()
		cursor.execute("select '12:01am-3:00am' as slot, count(1) as count from (select b.tym from (select str_to_date(a.date, '%m/%d/%Y %h:%i') as tym from crimedb a) b) c where str_to_date(c.tym, 'hh24:mi') between str_to_date('12:01','hh24:mi') and str_to_date('03:00','hh24:mi') group by '12:01am-3:00am' union select '09:01pm-12midnight' as slot, count(1) as count from (select b.tym from (select str_to_date(a.date, '%m/%d/%Y %h:%i') as tym from crimedb a) b) c where str_to_date(c.tym, 'hh24:mi') between str_to_date('21:01','hh24:mi') and str_to_date('00:00','hh24:mi') group by '09:01pm-12midnight' union select '3:01am-6:00am' as slot, count(1) as count from (select b.tym from (select str_to_date(a.date, '%m/%d/%Y %h:%i') as tym from crimedb a) b) c where str_to_date(c.tym, 'hh24:mi') between str_to_date('03:01','hh24:mi') and str_to_date('06:00','hh24:mi') group by '3:01am-6:00am' union select '6:01am-9:00am' as slot, count(1) as count from (select b.tym from (select str_to_date(a.date, '%m/%d/%Y %h:%i') as tym from crimedb a) b) c where str_to_date(c.tym, 'hh24:mi') between str_to_date('06:01','hh24:mi') and str_to_date('09:00','hh24:mi') group by '6:01am-9:00am' union select '9:01am-12:00noon' as slot, count(1) as count from (select b.tym from (select str_to_date(a.date, '%m/%d/%Y %h:%i') as tym from crimedb a) b) c where str_to_date(c.tym, 'hh24:mi') between str_to_date('09:01','hh24:mi') and str_to_date('12:00','hh24:mi') group by '9:01am-12:00noon' union select '12:01noon-3:00pm' as slot, count(1) as count from (select b.tym from (select str_to_date(a.date, '%m/%d/%Y %h:%i') as tym from crimedb a) b) c where str_to_date(c.tym, 'hh24:mi') between str_to_date('12:01','hh24:mi') and str_to_date('15:00','hh24:mi') group by '12:01noon-3:00pm' union select '3:01pm-6:00pm' as slot, count(1) as count from (select b.tym from (select str_to_date(a.date, '%m/%d/%Y %h:%i') as tym from crimedb a) b) c where str_to_date(c.tym, 'hh24:mi') between str_to_date('15:01','hh24:mi') and str_to_date('18:00','hh24:mi') group by '3:01pm-6:00pm' union select '6:01pm-9:00pm' as slot, count(1) as count from (select b.tym from (select str_to_date(a.date, '%m/%d/%Y %h:%i') as tym from crimedb a) b) c where str_to_date(c.tym, 'hh24:mi') between str_to_date('18:01','hh24:mi') and str_to_date('21:00','hh24:mi') group by '6:01pm-9:00pm'")
		data4 = cursor.fetchall()
		cursor.close()

		#-----Output Array------------------------------
		data = {
			Output(total_crime=data1,the_most_dangerous_street=data2,crime_type_count=data3,event_time_count=data4),
		}
		
		if data is not None:
        		return data
		else: 
			return "Not found"
		
class UserDefinedContext(object):
    def __init__(self, flask_config):
        self.config = flask_config


def create_app(flask_app):
    '''Creates SOAP services application and distribute Flask config into
    user con defined context for each method call.
    '''
    application = Application(
        [HelloWorldService], 'spyne.examples.flask',
        # The input protocol is set as HttpRpc to make our service easy to call.
        in_protocol=HttpRpc(validator='soft'),
        out_protocol=JsonDocument(ignore_wrappers=True),
    )
    # Use `method_call` hook to pass flask config to each service method
    # context. But if you have any better ideas do it, make a pull request.
    # NOTE. I refuse idea to wrap each call into Flask application context
    # because in fact we inside Spyne app context, not the Flask one.
    def _flask_config_context(ctx):
        ctx.udc = UserDefinedContext(flask_app.config)
    application.event_manager.add_listener('method_call', _flask_config_context)

    return application