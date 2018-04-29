

#import modules


import configparser, sys, os, datetime, time
from bson.objectid import ObjectId
import json


from pymongo import MongoClient

import cassandra
from cassandra.cqlengine import connection

import intermediate_transporter
import cassandra_dealer
from json_encoder import JSONEncoder

#set global constants


config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MONGO_DB_URL = os.environ.get('MONGO_DB_URL') if os.environ.get('MONGO_DB_URL') else config['MONGO']['host']
MONGO_DB_PORT = int(os.environ.get('MONGO_DB_PORT') if os.environ.get('MONGO_DB_PORT') else config['MONGO']['port'])
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') if os.environ.get('MONGO_DB_NAME') else config['MONGO']['db_name']

MAX_AGE = float(os.environ.get('MAX_AGE') or config['FRONTAL_TRANSPORTER']['max_age'])
CHECK_PERIOD = float(os.environ.get('CHECK_PERIOD') or config['FRONTAL_TRANSPORTER']['check_period'])

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


#make db connections


db = MongoClient(MONGO_DB_URL, MONGO_DB_PORT)[MONGO_DB_NAME]
connection.setup([item.lstrip().rstrip() for item in CASSANDRA_DB_URLS.split(CASSANDRA_HOST_DELIMITER)], CASSANDRA_DB_NAME)


## Move items according to collection and query one level up
def extract(params, collection):

	# Copy items from cassandra to mongo

	for item in connection.execute('select * from {0}.{1} {2};'.format(CASSANDRA_DB_NAME, collection, cassandra_dealer.querify(params, 'SELECT'))):
		db[collection].insert_one(cassandra_dealer.repair(item))

	# Copy items from lower levels to cassandra and mongo without replacing

	for item in intermediate_transporter.extract(params, collection):
		try:
			connection.execute('insert into {0}.{1} {2};'.format(CASSANDRA_DB_NAME, collection, cassandra_dealer.querify(item)))
		except Exception as e:
			pass
		
		try:
			db[collection].insert_one(item)
		except Exception as e:
			pass
	
	return


## Move item one level below
def immerse(item, collection, cause):
	item['__cause__'] = cause;
	connection.execute('insert into {0}.{1} {2};'.format(CASSANDRA_DB_NAME, collection, cassandra_dealer.querify(item)))
	db[collection].delete_one({'_id': ObjectId(item['_id'])})


## Check items inside collection and start moving them down if necessary
def inspect(collection, verbose = False):
	current_timestamp = datetime.datetime.now()
	current_timestamp_str = current_timestamp.strftime(TIMESTAMP_PATTERN)

	if verbose:
		print('{0} : inspecting {1}...'.format(current_timestamp_str, collection))
	
	for item in db[BOATS_COLLECTION_NAME].find():
		age = (current_timestamp - item['__accessed__']).total_seconds()

		if verbose:
			print('{0}{1} has not been accessed for {2} seconds'.format(' '*(len(current_timestamp_str) + 3), item['_id'], age))
		
		if age > MAX_AGE:

			if verbose:
				print('{0}{1} will be immersed'.format(' '*(len(current_timestamp_str) + 3), item['_id']))
			
			immerse(item, collection, 'too old')


## Get content of the lower level in json format
def get_content_on_lower():
	return JSONEncoder().encode({'boats' : extract({}, 'boats')})


## Start main loop
def main():
	print('Frontal transporter has started')
	verbose = '-v' in sys.argv
	once = '-o' in sys.argv
	while True:
		inspect(BOATS_COLLECTION_NAME, verbose = verbose)
		if once:
			return
		time.sleep(CHECK_PERIOD)

if __name__ == '__main__':
	main()
	#print(get_content_on_lower())