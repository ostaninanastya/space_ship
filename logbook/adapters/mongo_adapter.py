from pymongo import MongoClient
import configparser
import os

config = configparser.ConfigParser()
config.read('../databases.config')

MONGO_DB_URL = os.environ.get('MONGO_DB_URL') if os.environ.get('MONGO_DB_URL') else config['MONGO']['host']
MONGO_DB_PORT = int(os.environ.get('MONGO_DB_PORT') if os.environ.get('MONGO_DB_PORT') else config['MONGO']['port'])
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') if os.environ.get('MONGO_DB_NAME') else config['MONGO']['db_name']

db = MongoClient(MONGO_DB_URL, MONGO_DB_PORT)[MONGO_DB_NAME]

def is_valid_foreign_id(collection_name, id):
	return str(id) in [str(item['_id']) for item in db[collection_name].find({}, { '_id': 1 })]

if __name__ == '__main__':
	print(is_valid_foreign_id('127.0.0.1', 27017, 'test', 'system_test', '5abfbb95e1cd5bdb23b93336'))