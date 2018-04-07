from pymongo import MongoClient
import configparser
import os

from bson.objectid import ObjectId

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MONGO_DB_URL = os.environ.get('MONGO_DB_URL') if os.environ.get('MONGO_DB_URL') else config['MONGO']['host']
MONGO_DB_PORT = int(os.environ.get('MONGO_DB_PORT') if os.environ.get('MONGO_DB_PORT') else config['MONGO']['port'])
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') if os.environ.get('MONGO_DB_NAME') else config['MONGO']['db_name']

db = MongoClient(MONGO_DB_URL, MONGO_DB_PORT)[MONGO_DB_NAME]

def get_name_by_id(collection_name, id):
	return db[collection_name].find({'_id' : ObjectId(id)}, { 'name' : 1})[0]['name']


def get_all_ids(collection_name):
	return [str(item['_id']) for item in db[collection_name].find({}, { '_id': 1 })]

def is_valid_foreign_id(collection_name, id):
	return str(id) in get_all_ids(collection_name)

if __name__ == '__main__':
	print(get_name_by_id('system_test', '5abfcb1aa75ef28692553915'))
	#print(get_all_ids('system_test'))