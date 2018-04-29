

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


FIELD_DELIMITER = config['FIELDS']['field_delimiter']

fields = {
	'common': [item.lstrip().rstrip() for item in config['FIELDS']['common'].split(FIELD_DELIMITER)],
	'boats': [item.lstrip().rstrip() for item in config['FIELDS']['boats'].split(FIELD_DELIMITER)]
}


#make db connections


connection.setup([item.lstrip().rstrip() for item in CASSANDRA_DB_URLS.split(CASSANDRA_HOST_DELIMITER)], CASSANDRA_DB_NAME)

conn = connect_to_leader()
graph = Graph(bolt = True, user = conn['username'], password = conn['password'], host = conn['host'], bolt_port = conn['port'])
graph.begin()

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
	return JSONEncoder().encode({'boats' : extract({}, 'boats')})


## Move item one level below
def immerse(item, collection, cause):
	item['cause__'] = cause;

	#create item in neo4j with replacement
	
	delete_query = 'match (n:{0}) where space_ship.get_hex_ident(n._id) = "{1}" detach delete n;'.format(collection, cassandra_dealer.stringify(item['id'])[2:])
	graph.run(delete_query)
	
	create_query = 'create (n:{0} {{{1}}});'.format(collection, neo4j_dealer.querify(cassandra_dealer.repair(item), with_where = False, field_delimiter = ', '))
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
		inspect(BOATS_COLLECTION_NAME, verbose = verbose)
		if once:
			return
		time.sleep(CHECK_PERIOD)


if __name__ == '__main__':
	main()
	#print(extract({}, 'boats'))
	#print(get_content_on_lower())