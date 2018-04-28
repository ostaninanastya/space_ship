from pymongo import MongoClient, UpdateOne
import configparser
import sys, os, re
import datetime
from bson.objectid import ObjectId
import time

import cassandra
from cassandra.cqlengine import connection

import intermediate_transporter

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

db = MongoClient(MONGO_DB_URL, MONGO_DB_PORT)[MONGO_DB_NAME]

CASSANDRA_DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']
CASSANDRA_HOST_DELIMITER = os.environ.get('HOST_DELIMITER') if os.environ.get('HOST_DELIMITER') else config['CASSANDRA']['host_delimiter']
CASSANDRA_DB_URLS = os.environ.get('DB_URLS') if os.environ.get('DB_URLS') else config['CASSANDRA']['hosts']

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']
TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

connection.setup([item.lstrip().rstrip() for item in CASSANDRA_DB_URLS.split(CASSANDRA_HOST_DELIMITER)], CASSANDRA_DB_NAME)

def cassandra_stringify_value(value):
	if isinstance(value, datetime.datetime):
		return '\'' + value.strftime(TIMESTAMP_PATTERN) + '\''
	elif isinstance(value, list):
		return '\'' + str(value) + '\''
	elif isinstance(value, int) or isinstance(value, float):
		return str(value)
	elif isinstance(value, ObjectId):
		return '0x' + str(value)
	return '\'' + str(value) + '\''

def cassandra_querify(item, mode = 'INSERT'):
	querified = []
	for key in item:
		if item[key]:
			try:
				if key.index('__') == 0:
					querified.append([key[2:], cassandra_stringify_value(item[key])])
			except:
				try:
					if key.index('_') == 0:
						querified.append([key[1:], cassandra_stringify_value(item[key])])
				except:
					querified.append([key, cassandra_stringify_value(item[key])])
					continue

	if mode == 'INSERT':
		return '(' + ', '.join([item[0] for item in querified]) + ') values (' + ', '.join([item[1] for item in querified]) + ')'
	elif mode == 'SELECT':
		return ', '.join([item[0] + ' = ' + item[1] for item in querified])

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




def extract(params, collection):
	print(params)
	items = []
	for item in connection.execute('select * from {0}.{1} where {2} allow filtering;'.format(CASSANDRA_DB_NAME, collection, cassandra_querify(params, 'SELECT'))):
		repaired_item = cassandra_repair_fields(item)
		items.append(repaired_item)
		db[collection].insert_one(repaired_item)

	backended = intermediate_transporter.extract(params, collection)

	print(backended)

	for item in backended:
		try:
			connection.execute('insert into {0}.{1} {2};'.format(CASSANDRA_DB_NAME, collection, cassandra_querify(item)))
		except Exception as e:
			print(e)
		
		try:
			db[collection].insert_one(item)
		except Exception as e:
			print(e)
	
	return
	#print([cassandra_repair_fields(item) ])

def move(item, collection, cause):
	item['__cause__'] = cause;
	connection.execute('insert into {0}.{1} {2};'.format(CASSANDRA_DB_NAME, collection, cassandra_querify(item)))
	db[collection].delete_one({'_id': ObjectId(item['_id'])})

def show_ages(collection):
	current_timestamp = datetime.datetime.now()
	for item in db[BOATS_COLLECTION_NAME].find():
		age = (current_timestamp - item['__accessed__']).total_seconds()
		print('{0} has not been accessed for {1} seconds'.format(item['_id'], age))
		if age > MAX_AGE:
			print('Is goint to move')
			move(item, collection, 'too old')

def main():
	print('Frontal transporter has started')
	while True:
		show_ages(BOATS_COLLECTION_NAME)
		time.sleep(CHECK_PERIOD)

if __name__ == '__main__':
	main()