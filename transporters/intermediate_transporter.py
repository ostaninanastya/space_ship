import py2neo
from py2neo import Graph
import configparser
import sys, os, re
import datetime
from bson.objectid import ObjectId
import time

import rear_transporter

import cassandra
from cassandra.cqlengine import connection

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations/adapters/')

from mongo_adapter import mongo_str_id_to_int

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/connectors')
from neo4j_connector import connect_to_leader

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MAX_AGE = float(os.environ.get('MAX_AGE') or config['INTERMEDIATE_TRANSPORTER']['max_age'])
CHECK_PERIOD = float(os.environ.get('CHECK_PERIOD') or config['INTERMEDIATE_TRANSPORTER']['check_period'])

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

CASSANDRA_DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']
CASSANDRA_HOST_DELIMITER = os.environ.get('HOST_DELIMITER') if os.environ.get('HOST_DELIMITER') else config['CASSANDRA']['host_delimiter']
CASSANDRA_DB_URLS = os.environ.get('DB_URLS') if os.environ.get('DB_URLS') else config['CASSANDRA']['hosts']

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']
TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

connection.setup([item.lstrip().rstrip() for item in CASSANDRA_DB_URLS.split(CASSANDRA_HOST_DELIMITER)], CASSANDRA_DB_NAME)

conn = connect_to_leader()
graph = Graph(bolt = True, user = conn['username'], password = conn['password'], host = conn['host'], bolt_port = conn['port'])
graph.begin()

boats_fields = ['name', 'capacity']
common_fields = ['_id', '__accessed__', '__created__', '__gaps__']

def cassandra_stringify_value(value):
	if isinstance(value, datetime.datetime):
		return '\'' + value.strftime(TIMESTAMP_PATTERN) + '\''
	elif isinstance(value, list):
		return '\'' + str(value) + '\''
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

def cassandra_querify(item, mode = 'INSERT', keys = None):
	querified = []
	for key in item:
		if item[key] and (not keys or key in keys):
			try:
				if key.index('__') == 0:
					querified.append([key[2:], cassandra_stringify_value(item[key])])
				else:
					querified.append([key, cassandra_stringify_value(item[key])])
			except:
				try:
					if key.index('_') == 0:
						querified.append([key[1:], cassandra_stringify_value(item[key])])
					else:
						querified.append([key, cassandra_stringify_value(item[key])])
				except:
					querified.append([key, cassandra_stringify_value(item[key])])
					continue

	if mode == 'INSERT':
		return '(' + ', '.join([item[0] for item in querified]) + ') values (' + ', '.join([item[1] for item in querified]) + ')'
	elif mode == 'SELECT':
		return ', '.join([item[0] + ' = ' + item[1] for item in querified])
	elif mode == 'DELETE':
		return ' and '.join([item[0] + ' = ' + item[1] for item in querified])

def string_to_list(strlist):
	return [float(item.lstrip().rstrip()) for item in strlist.replace('[','').replace(']','').split(',')]

def cassandra_repair_fields(item):
	repaired = {}
	for key in item:
		if key == 'cause__':
			continue
		elif key == 'gaps__':
			repaired['__' + key] = string_to_list(item[key])
		else:
			try:
				if key.index('__') == len(key) - 2:
					repaired['__' + key] = item[key]
			except:
				if key == 'id':
					repaired['_' + key] = ObjectId(item[key])
				else:
					repaired[key] = item[key]

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

	for item in rear_transporter.extract(params, collection):
		try:
			query = 'create (n:{0} {{{1}}});'.format(collection, neo4j_querify(item, field_delimiter = ', '))
			graph.run(query)
		except py2neo.database.status.ConstraintError as e:
			print(e)

	print('match (n:{0}) where {1} return {2};'.format(collection, 
		neo4j_querify(params, prefix = 'n.', delimiter = ' = '), 
		(', '.join(['n.' + item for item in boats_fields + common_fields])).replace('n._id', 'space_ship.get_hex_ident(n._id) as _id')))
	return [neo4j_repair_fields(item) for item in graph.run('match (n:{0}) where {1} return {2};'.format(collection, 
		neo4j_querify(params, prefix = 'n.', delimiter = ' = '), 
		(', '.join(['n.' + item for item in boats_fields + common_fields])).replace('n._id', 'space_ship.get_hex_ident(n._id) as _id')))]

def move(item, collection, cause):
	item['cause__'] = cause;
	print(item)
	try:
		query = 'create (n:{0} {{{1}}});'.format(collection, neo4j_querify(cassandra_repair_fields(item), field_delimiter = ', '))
		graph.run(query)
	except py2neo.database.status.ConstraintError:
		query = 'match (n:{0}) where space_ship.get_hex_ident(n._id) = "{1}" detach delete n;'.format(collection, cassandra_stringify_value(item['id'])[2:])
		#query = 'match (n:{0}) where {1} detach delete n;'.format(collection, neo4j_querify(cassandra_repair_fields(item), delimiter = ' = ', field_delimiter = ' and '))
		graph.run(query)
		query = 'create (n:{0} {{{1}}});'.format(collection, neo4j_querify(cassandra_repair_fields(item), field_delimiter = ', '))
		graph.run(query)
	#print('\n\n', query, '\n\n')
	#graph.run(query)
	print('delete from {0}.{1} where {2} allow filtering;'.format(CASSANDRA_DB_NAME, collection, cassandra_querify(item, 'DELETE')))
	connection.execute('delete from {0}.{1} where {2};'.format(CASSANDRA_DB_NAME, collection, cassandra_querify(item, 'DELETE', keys = ['id', 'name'])))
	#db[collection].delete_one({'_id': ObjectId(item['_id'])})

def show_ages(collection):
	current_timestamp = datetime.datetime.now()
	for item in connection.execute('select * from {0}.{1};'.format(CASSANDRA_DB_NAME, collection)):
		age = (current_timestamp - item['accessed__']).total_seconds()
		print('{0} has not been accessed for {1} seconds'.format(item['id'], age))
		if age > MAX_AGE:
			print('Is going to move')
			move(item, collection, 'too old')

def main():
	print('Intermediate transporter has started')
	while True:
		show_ages(BOATS_COLLECTION_NAME)
		time.sleep(CHECK_PERIOD)

if __name__ == '__main__':
	main()
	#extract({'name' : 'Third'}, 'boats')