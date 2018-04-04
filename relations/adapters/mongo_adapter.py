from pymongo import MongoClient
import configparser
import os, re

config = configparser.ConfigParser()
config.read('../databases.config')

MONGO_DB_URL = os.environ.get('MONGO_DB_URL') if os.environ.get('MONGO_DB_URL') else config['MONGO']['host']
MONGO_DB_PORT = int(os.environ.get('MONGO_DB_PORT') if os.environ.get('MONGO_DB_PORT') else config['MONGO']['port'])
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') if os.environ.get('MONGO_DB_NAME') else config['MONGO']['db_name']

db = MongoClient(MONGO_DB_URL, MONGO_DB_PORT)[MONGO_DB_NAME]

def splitword(w):
    print('got word', w)
    split = -((-len(w))//2)
    return w[:split], w[split:]

def int_to_mongo_str_id(values):

	result = []

	for value in values:
		result.append((value).to_bytes(6, byteorder='big').hex())

	return ''.join(result)

def mongo_str_id_to_int(value):
    values = splitword(value)
    result = []
    for value in values:
        result.append(int.from_bytes(bytearray.fromhex(' '.join(re.findall('..', value))), 'big'))
    return tuple(result)

def is_valid_foreign_id(collection_name, id):
	return str(id) in [str(item['_id']) for item in db[collection_name].find({}, { '_id': 1 })]

def validate_id(collection_name, id):
    if isinstance(id, str):
            if is_valid_foreign_id(collection_name, id):
                return mongo_str_id_to_int(id)
            else:
                raise ValueError('invalid {0} id'.format(collection_name))
    else:
        return id

if __name__ == '__main__':
	print(is_valid_foreign_id('127.0.0.1', 27017, 'test', 'system_test', '5abfbb95e1cd5bdb23b93336'))