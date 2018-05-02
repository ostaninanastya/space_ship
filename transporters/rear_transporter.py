

#import modules


import configparser, sys, os, re, datetime, time
from bson.objectid import ObjectId
import numpy
import json

import py2neo
from py2neo import Graph
import mysql.connector

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations/adapters/')
from mongo_adapter import mongo_str_id_to_int
sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/connectors')
from neo4j_connector import connect_to_leader
import neo4j_dealer
import mysql_dealer
from json_encoder import JSONEncoder


#set global constants


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

MYSQL_DB_NAME = os.environ.get('MYSQL_DB_NAME') if os.environ.get('MYSQL_DB_NAME') else config['MYSQL']['db_name']

FIELD_DELIMITER = config['FIELDS']['field_delimiter']

fields = {
	'common': [item.lstrip().rstrip() for item in config['FIELDS']['common'].split(FIELD_DELIMITER)],
	'boats': [item.lstrip().rstrip() for item in config['FIELDS']['boats'].split(FIELD_DELIMITER)]
}

MYSQL_FIELD_DELIMITER = config['MYSQL_FIELDS']['field_delimiter']

mysql_fields = {
	'boats': [item.lstrip().rstrip() for item in config['MYSQL_FIELDS']['boats'].split(MYSQL_FIELD_DELIMITER)]
}


#make db connections


connection = mysql.connector.connect(user='root', password='cassadaga', host='127.0.0.1', database = MYSQL_DB_NAME)

conn = connect_to_leader()
graph = Graph(bolt = True, user = conn['username'], password = conn['password'], host = conn['host'], bolt_port = conn['port'])
graph.begin()

## Move items according to collection and query one level up
def extract(params, collection):
	items = []

	cursor = connection.cursor()
	cursor.execute('select * from {0} {1};'.format(collection, mysql_dealer.querify(params, mode = 'SELECT')))

	# Return found items to upper level
	
	return [mysql_dealer.repair(item, mysql_fields[collection]) for item in cursor]


## Move item one level below
def immerse(item, collection, cause):
	item['__cause__'] = cause;
	
	cursor = connection.cursor()

	#create item in mysql with replacement

	cursor.execute('delete from {0} where {1};'.format(collection, mysql_dealer.querify(item, mode = 'DELETE', keys = ['_id'])))
	cursor.execute('insert into {0} {1};'.format(collection, mysql_dealer.querify(item)))

	connection.commit()

	#delete item from neo4j

	delete_query = 'match (n:{0}) where space_ship.get_hex_ident(n._id) = "{1}" detach delete n;'.format(collection, mysql_dealer.stringify(item['_id'])[2:])
	graph.run(delete_query)


## Get average frequency by last timestamp, set of gaps and length of interval for counting frequency
def get_frequency(last_timestamp, gaps, interval_length):
	current_timestamp = datetime.datetime.now()
	gaps.append((current_timestamp - last_timestamp).total_seconds())

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

		frequencies.append(number_of_requests)

	return numpy.average(frequencies)


## Check items inside collection and start moving them down if necessary
def inspect(collection, verbose = False):
	current_timestamp = datetime.datetime.now()
	current_timestamp_str = current_timestamp.strftime(TIMESTAMP_PATTERN)

	if verbose:
		print('{0} : inspecting {1}...'.format(current_timestamp_str, collection))

	for item in graph.run('match (n:{0}) return {1};'.format(collection, 
		(', '.join(['n.' + item for item in fields['common'] + fields[collection]])).replace('n._id', 'space_ship.get_hex_ident(n._id) as _id'))):

		repaired_item = neo4j_dealer.repair(item)

		frequency = get_frequency(last_timestamp = repaired_item['__accessed__'], gaps = repaired_item['__gaps__'], interval_length = CHECK_INTERVAL)

		if verbose:
			print('{0}{1} has been accessed with frequency {1} times per {2} seconds'.format(' '*(len(current_timestamp_str) + 3),
			repaired_item['_id'], frequency, CHECK_INTERVAL))

		if frequency < MIN_FREQUENCY:

			if verbose:
				print('{0}{1} will be immersed'.format(' '*(len(current_timestamp_str) + 3), repaired_item['_id']))
			
			immerse(repaired_item, collection, 'too rarely accessed')


## Get content of the lower level in json format
def get_content_on_lower():
	return JSONEncoder().encode({'boats' : extract({}, 'boats')})


## Start main loop
def main():
	print('Rear transporter has started')
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