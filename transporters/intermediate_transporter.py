

#import modules


import configparser, sys, os, re, datetime
from bson.objectid import ObjectId
import time
import json

import cassandra
from cassandra.cqlengine import connection

import py2neo
from py2neo import Graph

import rear_transporter

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/connectors')
from neo4j_connector import connect_to_leader
import cassandra_dealer
import neo4j_dealer
from json_encoder import JSONEncoder


#set global constants


config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MAX_AGE = float(os.environ.get('MAX_AGE') or config['INTERMEDIATE_TRANSPORTER']['max_age'])
CHECK_PERIOD = float(os.environ.get('CHECK_PERIOD') or config['INTERMEDIATE_TRANSPORTER']['check_period'])

# recital
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
# relations
SHIFTS_COLLECTION_NAME = os.environ.get('SHIFTS_COLLECTION_NAME') or config['MONGO']['shifts_collection_name']
OPERATIONS_COLLECTION_NAME = os.environ.get('OPERATIONS_COLLECTION_NAME') or config['MONGO']['operations_collection_name']
REQUIREMENTS_COLLECTION_NAME = os.environ.get('REQUIREMENTS_COLLECTION_NAME') or config['MONGO']['requirements_collection_name']
# logbook
SYSTEM_TESTS_COLLECTION_NAME = os.environ.get('SYSTEM_TESTS_COLLECTION_NAME') or config['MONGO']['system_tests_collection_name']
CONTROL_ACTIONS_COLLECTION_NAME = os.environ.get('CONTROL_ACTIONS_COLLECTION_NAME') or config['MONGO']['control_actions_collection_name']
POSITIONS_COLLECTION_NAME = os.environ.get('POSITIONS_COLLECTION_NAME') or config['MONGO']['positions_collection_name']
SENSOR_DATA_COLLECTION_NAME = os.environ.get('SENSOR_DATA_COLLECTION_NAME') or config['MONGO']['sensor_data_collection_name']
SHIFT_STATES_COLLECTION_NAME = os.environ.get('SHIFT_STATES_COLLECTION_NAME') or config['MONGO']['shift_states_collection_name']
OPERATION_STATES_COLLECTION_NAME = os.environ.get('OPERATION_STATES_COLLECTION_NAME') or config['MONGO']['operation_states_collection_name']

CASSANDRA_DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']
CASSANDRA_HOST_DELIMITER = os.environ.get('HOST_DELIMITER') if os.environ.get('HOST_DELIMITER') else config['CASSANDRA']['host_delimiter']
CASSANDRA_DB_URLS = os.environ.get('DB_URLS') if os.environ.get('DB_URLS') else config['CASSANDRA']['hosts']

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']
TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']


FIELD_DELIMITER = config['FIELDS']['field_delimiter']

fields = {
	# recital
	'common': [item.lstrip().rstrip() for item in config['FIELDS']['common'].split(FIELD_DELIMITER)],
	'boats': [item.lstrip().rstrip() for item in config['FIELDS']['boats'].split(FIELD_DELIMITER)],
	'property_types': [item.lstrip().rstrip() for item in config['FIELDS']['property_types'].split(FIELD_DELIMITER)],
	'system_states': [item.lstrip().rstrip() for item in config['FIELDS']['system_states'].split(FIELD_DELIMITER)],
	'system_types': [item.lstrip().rstrip() for item in config['FIELDS']['system_types'].split(FIELD_DELIMITER)],
	'specializations': [item.lstrip().rstrip() for item in config['FIELDS']['specializations'].split(FIELD_DELIMITER)],
	'locations': [item.lstrip().rstrip() for item in config['FIELDS']['locations'].split(FIELD_DELIMITER)],
	'sensors': [item.lstrip().rstrip() for item in config['FIELDS']['sensors'].split(FIELD_DELIMITER)],
	'systems': [item.lstrip().rstrip() for item in config['FIELDS']['systems'].split(FIELD_DELIMITER)],
	'people': [item.lstrip().rstrip() for item in config['FIELDS']['people'].split(FIELD_DELIMITER)],
	'departments': [item.lstrip().rstrip() for item in config['FIELDS']['departments'].split(FIELD_DELIMITER)],
	'properties': [item.lstrip().rstrip() for item in config['FIELDS']['properties'].split(FIELD_DELIMITER)],
	# relations
	'shifts': [item.lstrip().rstrip() for item in config['FIELDS']['shifts'].split(FIELD_DELIMITER)],
	'operations': [item.lstrip().rstrip() for item in config['FIELDS']['operations'].split(FIELD_DELIMITER)],
	'requirements': [item.lstrip().rstrip() for item in config['FIELDS']['requirements'].split(FIELD_DELIMITER)],
	# logbook
	'system_tests': [item.lstrip().rstrip() for item in config['FIELDS']['system_tests'].split(FIELD_DELIMITER)],
	'control_actions': [item.lstrip().rstrip() for item in config['FIELDS']['control_actions'].split(FIELD_DELIMITER)],
	'positions': [item.lstrip().rstrip() for item in config['FIELDS']['positions'].split(FIELD_DELIMITER)],
	'sensor_data': [item.lstrip().rstrip() for item in config['FIELDS']['sensor_data'].split(FIELD_DELIMITER)],
	'shift_states': [item.lstrip().rstrip() for item in config['FIELDS']['shift_states'].split(FIELD_DELIMITER)],
	'operation_states': [item.lstrip().rstrip() for item in config['FIELDS']['operation_states'].split(FIELD_DELIMITER)]
}

#make db connections


connection.setup([item.lstrip().rstrip() for item in CASSANDRA_DB_URLS.split(CASSANDRA_HOST_DELIMITER)], CASSANDRA_DB_NAME)

conn = connect_to_leader()
graph = Graph(bolt = True, user = conn['username'], password = conn['password'], host = conn['host'], bolt_port = conn['port'])
graph.begin()

def remove(collection, item):
	rear_transporter.remove(collection, item)
	query = 'match (n:{0}) where space_ship.get_hex_ident(n._id) = "{1}" detach delete n;'.format(collection, cassandra_dealer.stringify(item['_id'])[2:])
	#print(query)
	graph.run(query)

## Move items according to collection and query one level up
def extract(params, collection):
	items = []

	# Copy items from lower level to neo4j without replacing

	for item in rear_transporter.extract(params, collection):
		try:
			create_query = 'create (n:{0} {{{1}}});'.format(collection, neo4j_dealer.querify(item, with_where = False, field_delimiter = ', '))
			graph.run(create_query)
		except py2neo.database.status.ConstraintError as e:
			pass

	# Return found items to upper level

	return [neo4j_dealer.repair(item) for item in graph.run(
			'match (n:{0}) {1} return {2};'.format(
				collection, 
				neo4j_dealer.querify(params, prefix = 'n.', delimiter = ' = '), 
				(', '.join(['n.' + item for item in fields['common'] + fields[collection]])).replace('n._id', 'space_ship.get_hex_ident(n._id) as _id')))]


## Get content of the lower level in json format
def get_content_on_lower():
	collections = [BOATS_COLLECTION_NAME, PROPERTY_TYPES_COLLECTION_NAME, SYSTEM_STATES_COLLECTION_NAME, SYSTEM_TYPES_COLLECTION_NAME,
	SPECIALIZATIONS_COLLECTION_NAME, LOCATIONS_COLLECTION_NAME, SENSORS_COLLECTION_NAME, SYSTEMS_COLLECTION_NAME, PEOPLE_COLLECTION_NAME,
	DEPARTMENTS_COLLECTION_NAME, PROPERTIES_COLLECTION_NAME, SHIFTS_COLLECTION_NAME, OPERATIONS_COLLECTION_NAME, REQUIREMENTS_COLLECTION_NAME,
	SYSTEM_TESTS_COLLECTION_NAME, CONTROL_ACTIONS_COLLECTION_NAME, POSITIONS_COLLECTION_NAME, SENSOR_DATA_COLLECTION_NAME,
	SHIFT_STATES_COLLECTION_NAME, OPERATION_STATES_COLLECTION_NAME]

	result = {}

	for collection in collections:
		result[collection] = extract({}, collection)

	return result


## Move item one level below
def immerse(item, collection, cause):
	item['cause__'] = cause;

	#create item in neo4j with replacement
	
	delete_query = 'match (n:{0}) where space_ship.get_hex_ident(n._id) = "{1}" detach delete n;'.format(collection, cassandra_dealer.stringify(item['id'])[2:])
	graph.run(delete_query)

	print(cassandra_dealer.repair(item))
	
	create_query = 'create (n:{0} {{{1}}});'.format(collection, neo4j_dealer.querify(cassandra_dealer.repair(item), with_where = False, field_delimiter = ', '))
	print(create_query)
	graph.run(create_query)

	#delete item from cassandra

	connection.execute('delete from {0}.{1} where {2};'.format(CASSANDRA_DB_NAME, collection, cassandra_dealer.querify(item, 'DELETE', keys = ['id', 'name'])))


## Check items inside collection and start moving them down if necessary
def inspect(collection, verbose = False):
	current_timestamp = datetime.datetime.now()
	current_timestamp_str = current_timestamp.strftime(TIMESTAMP_PATTERN)

	if verbose:
		print('{0} : inspecting {1}...'.format(current_timestamp_str, collection))

	for item in connection.execute('select * from {0}.{1};'.format(CASSANDRA_DB_NAME, collection)):
		age = (current_timestamp - item['accessed__']).total_seconds()

		if verbose:
			print('{0}{1} has not been accessed for {2} seconds'.format(' '*(len(current_timestamp_str) + 3), item['id'].hex(), age))

		if age > MAX_AGE:

			if verbose:
				print('{0}{1} will be immersed'.format(' '*(len(current_timestamp_str) + 3), item['id'].hex()))
			
			immerse(item, collection, 'too old')


## Start main loop
def main():
	print('Intermediate transporter has started')
	verbose = '-v' in sys.argv
	once = '-o' in sys.argv
	while True:
		# recital
		inspect(BOATS_COLLECTION_NAME, verbose = verbose)
		inspect(PROPERTY_TYPES_COLLECTION_NAME, verbose = verbose)
		inspect(SYSTEM_STATES_COLLECTION_NAME, verbose = verbose)
		inspect(SYSTEM_TYPES_COLLECTION_NAME, verbose = verbose)
		inspect(SPECIALIZATIONS_COLLECTION_NAME, verbose = verbose)
		inspect(LOCATIONS_COLLECTION_NAME, verbose = verbose)
		inspect(SENSORS_COLLECTION_NAME, verbose = verbose)
		inspect(SYSTEMS_COLLECTION_NAME, verbose = verbose)
		inspect(PEOPLE_COLLECTION_NAME, verbose = verbose)
		inspect(DEPARTMENTS_COLLECTION_NAME, verbose = verbose)
		inspect(PROPERTIES_COLLECTION_NAME, verbose = verbose)
		# relations
		inspect(SHIFTS_COLLECTION_NAME, verbose = verbose)
		inspect(OPERATIONS_COLLECTION_NAME, verbose = verbose)
		inspect(REQUIREMENTS_COLLECTION_NAME, verbose = verbose)
		# logbook
		inspect(SYSTEM_TESTS_COLLECTION_NAME, verbose = verbose)
		inspect(CONTROL_ACTIONS_COLLECTION_NAME, verbose = verbose)
		inspect(POSITIONS_COLLECTION_NAME, verbose = verbose)
		inspect(SENSOR_DATA_COLLECTION_NAME, verbose = verbose)
		inspect(SHIFT_STATES_COLLECTION_NAME, verbose = verbose)
		inspect(OPERATION_STATES_COLLECTION_NAME, verbose = verbose)
		if once:
			return
		time.sleep(CHECK_PERIOD)


if __name__ == '__main__':
	main()
	#print(extract({}, 'boats'))
	#print(get_content_on_lower())