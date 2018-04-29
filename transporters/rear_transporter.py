import py2neo
from py2neo import Graph
import configparser
import sys, os, re
import datetime
from bson.objectid import ObjectId
import time
import numpy

import cassandra
from cassandra.cqlengine import connection

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations/adapters/')

from mongo_adapter import mongo_str_id_to_int

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/connectors')
from neo4j_connector import connect_to_leader
import mysql.connector
import pickle


config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MIN_FREQUENCY = float(os.environ.get('MIN_FREQUENCY') or config['REAR_TRANSPORTER']['min_frequency'])
CHECK_INTERVAL = float(os.environ.get('CHECK_INTERVAL') or config['REAR_TRANSPORTER']['check_interval'])
CHECK_PERIOD = float(os.environ.get('CHECK_PERIOD') or config['REAR_TRANSPORTER']['check_period'])

BOATS_COLLECTION_NAME = os.environ.get('BOATS_COLLECTION_NAME') or config['MONGO']['boats_collection_name']
DEPARTMENTS_COLLECTION_NAME = os.environ.get('DEPARTMENTS_COLLECTION_NAME') or config['MONGO']['departments_collection_name']
LOCATIONS_COLLECTION_NAME = os.environ.get('LOCATIONS_COLLECTION_NAME') or config['MONGO']['locations_collection_name']
PEOPLE_COLLECTION_NAME = os.environ.get('PEOPLE_COLLECTION_NAME') or config['MONGO']['people_collection_name']
PROPERTIES_COLLECTION_NAME = os.environ.get('PROPERTIES_COLLECTION_NAME') or config['MONGO']['properties_collection_name']
PROPERTY_TYPES_COLLECTION_NAME = os.environ.get('PROPERTY_TYPES_COLLECTION_NAME') or config['MONGO']['property_types_collection_name']
SENSORS_COLLECTION_NAME = os.environ.get('SENSORS_COLLECTION_NAME') or config['MONGO']['sensors_collection_name']
SPECIALIZATIONS_COLLECTION_NAME = os.environ.get('SPECIALIZATIONS_COLLECTION_NAME') or config['MONGO']['specializations_collection_name']
SYSTEM_STATES_COLLECTION_NAME = os.environ.get('SYSTEM_STATES_COLLECTION_NAME') or config['MONGO']['system_states_collection_name']
SYSTEM_TYPES_COLLECTION_NAME = os.environ.get('SYSTEM_TYPES_COLLECTION_NAME') or config['MONGO']['system_types_collection_name']
SYSTEMS_COLLECTION_NAME = os.environ.get('SYSTEMS_COLLECTION_NAME') or config['MONGO']['systems_collection_name']

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']
TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

conn = connect_to_leader()
graph = Graph(bolt = True, user = conn['username'], password = conn['password'], host = conn['host'], bolt_port = conn['port'])
graph.begin()

boats_fields = ['name', 'capacity']
common_fields = ['_id', '__accessed__', '__created__', '__gaps__']

mysql_fields = ['_id', 'name', 'capacity', '__created__', '__accessed__', '__gaps__']

MYSQL_DB_NAME = os.environ.get('MYSQL_DB_NAME') if os.environ.get('MYSQL_DB_NAME') else config['MYSQL']['db_name']

connection = mysql.connector.connect(user='root', password='cassadaga', host='127.0.0.1', database = MYSQL_DB_NAME)

def mysql_stringify_value(value):
	if isinstance(value, datetime.datetime):
		return '\'' + value.strftime(TIMESTAMP_PATTERN) + '\''
	elif isinstance(value, list):
		return '0x' + pickle.dumps(value).hex()
	elif isinstance(value, int) or isinstance(value, float):
		return str(value)
	elif isinstance(value, ObjectId):
		return '0x' + str(value)
	elif isinstance(value, bytearray) or isinstance(value, bytes):
		return '0x' + value.hex()
	return '\'' + str(value) + '\''

def neo4j_stringify_value(value):
	#print(value)
	if isinstance(value, datetime.datetime):
		return '\'' + value.strftime(TIMESTAMP_PATTERN) + '\''
	elif isinstance(value, int) or isinstance(value, float) or isinstance(value, list):
		return str(value)
	elif isinstance(value, ObjectId):
		return  str(list(mongo_str_id_to_int(str(value))))
	return '\'' + str(value) + '\''

def neo4j_querify(item, prefix = '', delimiter = ' : ', field_delimiter = ' and '):
	querified = []
	for key in item:
		if item[key]:
			querified.append([key, neo4j_stringify_value(item[key])])

	return field_delimiter.join([prefix + item[0] + delimiter + item[1] for item in querified])

def mysql_querify(item, mode = 'INSERT', keys = None):
	querified = []
	for key in item:
		if item[key] and (not keys or key in keys):
			querified.append([key, mysql_stringify_value(item[key])])
			continue

	if mode == 'INSERT':
		return '(' + ', '.join([item[0] for item in querified]) + ') values (' + ', '.join([item[1] for item in querified]) + ')'
	elif mode == 'SELECT':
		return ', '.join([item[0] + ' = ' + item[1] for item in querified])
	elif mode == 'DELETE':
		return ' and '.join([item[0] + ' = ' + item[1] for item in querified])

def string_to_list(strlist):
	return [float(item.lstrip().rstrip()) for item in strlist.replace('[','').replace(']','').split(',')]

def mysql_repair_fields(item, field_names):
	repaired = {}
	index = 0
	for key in field_names:
		if key == '__gaps__':
			repaired[key] = pickle.loads(item[index])
		elif key == '_id':
			repaired[key] = ObjectId(item[index])
		else:
			repaired[key] = item[index]

		index += 1
					

	return repaired


def neo4j_repair_fields(item):
	repaired = {}
	for key in dict(item):
		value = item[key]
		if key == '_id':
			value = ObjectId(item[key])
		else:
			try:
				value = datetime.datetime.strptime(value, TIMESTAMP_PATTERN)
			except:
				pass
		repaired[key.replace('n.', '')] = value

	return repaired


def extract(params, collection):
	items = []

	cursor = connection.cursor()

	cursor.execute('select * from {0} where {1};'.format(collection, mysql_querify(params, mode = 'SELECT')))
	
	return [mysql_repair_fields(item, mysql_fields) for item in cursor]

	#print('match (n:{0}) where {1} return {2};'.format(collection, 
	#	neo4j_querify(params, prefix = 'n.', delimiter = ' = '), 
	#	(', '.join(['n.' + item for item in boats_fields + common_fields])).replace('n._id', 'space_ship.get_hex_ident(n._id) as _id')))
	
	#return [neo4j_repair_fields(item) for item in graph.run('match (n:{0}) where {1} return {2};'.format(collection, 
	#	neo4j_querify(params, prefix = 'n.', delimiter = ' = '), 
	#	(', '.join(['n.' + item for item in boats_fields + common_fields])).replace('n._id', 'space_ship.get_hex_ident(n._id) as _id')))]

def move(item, collection, cause):
	item['__cause__'] = cause;
	print(item)
	
	cursor = connection.cursor()

	try:
		cursor.execute('insert into {0} {1};'.format(collection, mysql_querify(item)))
		print('insert into {0} {1};'.format(collection, mysql_querify(item)))
	except mysql.connector.errors.IntegrityError as e:
		print(e)
		cursor.execute('delete from {0} where {1};'.format(collection, mysql_querify(item, mode = 'DELETE', keys = ['_id'])))
		print('insert into {0} {1};'.format(collection, mysql_querify(item)))
		cursor.execute('insert into {0} {1};'.format(collection, mysql_querify(item)))

	connection.commit()

	query = 'match (n:{0}) where space_ship.get_hex_ident(n._id) = "{1}" detach delete n;'.format(collection, mysql_stringify_value(item['_id'])[2:])
	graph.run(query)
	
	#try:
	#	query = 'create (n:{0} {{{1}}});'.format(collection, neo4j_querify(cassandra_repair_fields(item), field_delimiter = ', '))
	#	graph.run(query)
	#except py2neo.database.status.ConstraintError:
	#	query = 'match (n:{0}) where space_ship.get_hex_ident(n._id) = "{1}" detach delete n;'.format(collection, cassandra_stringify_value(item['id'])[2:])
		#query = 'match (n:{0}) where {1} detach delete n;'.format(collection, neo4j_querify(cassandra_repair_fields(item), delimiter = ' = ', field_delimiter = ' and '))
	#	graph.run(query)
	#	query = 'create (n:{0} {{{1}}});'.format(collection, neo4j_querify(cassandra_repair_fields(item), field_delimiter = ', '))
	#	graph.run(query)
	#print('\n\n', query, '\n\n')
	#graph.run(query)
	#print('delete from {0}.{1} where {2} allow filtering;'.format(CASSANDRA_DB_NAME, collection, cassandra_querify(item, 'DELETE')))
	#connection.execute('delete from {0}.{1} where {2};'.format(CASSANDRA_DB_NAME, collection, cassandra_querify(item, 'DELETE', keys = ['id', 'name'])))
	#db[collection].delete_one({'_id': ObjectId(item['_id'])})

def get_frequency(last_timestamp, gaps, interval_length):
	current_timestamp = datetime.datetime.now()
	gaps.append((current_timestamp - last_timestamp).total_seconds())

	#print(gaps)

	gaps_sum = numpy.sum(gaps)
	
	frequencies = []

	current_gap = 2

	current_low_bound = 0
	current_up_bound = interval_length

	distance = gaps[-current_gap]

	while (current_gap < len(gaps)) and ((current_up_bound < gaps_sum) or (current_low_bound == 0)):
		number_of_requests = 0

		while (current_gap < len(gaps)) and distance + gaps[-current_gap] >= current_low_bound and distance + gaps[-current_gap] < current_up_bound:
			number_of_requests += 1
			distance += gaps[-current_gap]
			current_gap += 1

		current_low_bound += interval_length
		current_up_bound += interval_length

		#while (distance < interval_length) and (current_gap < len(gaps)):
		#	number_of_requests += 1
		#	current_gap += 1
		#	distance += gaps[-current_gap]

		frequencies.append(number_of_requests)

	#frequencies.reverse()

	return numpy.average(frequencies)	


def show_ages(collection):
	current_timestamp = datetime.datetime.now()
	for item in graph.run('match (n:{0}) return {1};'.format(collection, 
		(', '.join(['n.' + item for item in boats_fields + common_fields])).replace('n._id', 'space_ship.get_hex_ident(n._id) as _id'))):

		repaired_item = neo4j_repair_fields(item)

		#age = (current_timestamp - repaired_item['__accessed__']).total_seconds()

		frequency = get_frequency(last_timestamp = repaired_item['__accessed__'], gaps = repaired_item['__gaps__'], interval_length = CHECK_INTERVAL)

		print('{0} has been accessed with frequency {1} times per {2} seconds'.format(repaired_item['_id'], frequency, CHECK_INTERVAL))
		if frequency < MIN_FREQUENCY:
			print('Is going to move')
			move(repaired_item, collection, 'too rarely accessed')

def main():
	print('Rear transporter has started')
	while True:
		show_ages(BOATS_COLLECTION_NAME)
		time.sleep(CHECK_PERIOD)

if __name__ == '__main__':
	main()
	#print(extract({'name' : 'Third'}, 'boats'))