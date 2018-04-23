import os,sys

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/generation')

from json_mongo_corrector import convert

import configparser

from subprocess import call

from pymongo import MongoClient

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MONGO_DB_URL = os.environ.get('MONGO_DB_URL') if os.environ.get('MONGO_DB_URL') else config['MONGO']['host']
MONGO_DB_PORT = int(os.environ.get('MONGO_DB_PORT') if os.environ.get('MONGO_DB_PORT') else config['MONGO']['port'])
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') if os.environ.get('MONGO_DB_NAME') else config['MONGO']['db_name']

db = MongoClient(MONGO_DB_URL, MONGO_DB_PORT)[MONGO_DB_NAME]

print(db)

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

def fill(collection, base, foreign_ids = []):
	db[collection].delete_many({})
	print(call(['mongoimport','--port',str(MONGO_DB_PORT),'--db', MONGO_DB_NAME, '--collection', collection, '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/mongo json/{0}.json'.format(base), base, foreign_ids)]))

if __name__ == '__main__':
	fill(BOATS_COLLECTION_NAME, 'boats')
	fill(DEPARTMENTS_COLLECTION_NAME, 'department')
	fill(LOCATIONS_COLLECTION_NAME, 'locations')
	fill(PEOPLE_COLLECTION_NAME, 'people', ['specialization', 'department'])
	fill(PROPERTIES_COLLECTION_NAME, 'properties', ['type', 'department'])
	fill(PROPERTY_TYPES_COLLECTION_NAME, 'propertyTypes')
	fill(SENSORS_COLLECTION_NAME, 'sensors', ['location'])
	fill(SPECIALIZATIONS_COLLECTION_NAME, 'specializations')
	fill(SYSTEM_STATES_COLLECTION_NAME, 'states')
	fill(SYSTEM_TYPES_COLLECTION_NAME, 'systemTypes')
	fill(SYSTEMS_COLLECTION_NAME, 'systems', ['type', 'state', 'personInCharge'])

