import os,sys
import json

from cassandra.cqlengine import connection

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/generation')

from json_cassandra_corrector import convert

import configparser

from subprocess import call

from pymongo import MongoClient

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host'] 
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

connection.setup([DB_URL], DB_NAME)

def fill(entity_name, base, batch_size, mongo_ids = [], neo_ids = [], strings = []):
	data = json.load(open(convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/cassandra json/{0}.json'.format(base), base, mongo_ids = mongo_ids,
		neo_ids = neo_ids, strings = strings)))

	number_of_batches = (len(data["data"]) // batch_size) + 1

	for i in range(number_of_batches + 1):
		if i < number_of_batches:	
			query = "BEGIN BATCH {0} APPLY BATCH;".format(' '.join(
				["insert into {0}.{1} json '{2}';".format(DB_NAME, entity_name, json.dumps(item)) for item in data["data"][i*batch_size : (i + 1)*batch_size]]))
		else:
			query = "BEGIN BATCH {0} APPLY BATCH;".format(' '.join(
				["insert into {0}.{1} json '{2}';".format(DB_NAME, entity_name, json.dumps(item)) for item in data["data"][i*batch_size :]]))
		print(connection.execute(query))

if __name__ == '__main__':
	#fill(entity_name = 'system_test', base = 'system_test', batch_size = 100, mongo_ids = ['system'])
	#fill(entity_name = 'control_action', base = 'control_action', batch_size = 2, mongo_ids = ['user_id'], neo_ids = [], strings = ['result'])
	#fill(entity_name = 'position', base = 'position', batch_size = 100)
	#fill(entity_name = 'operation_state', base = 'operation_state', batch_size = 5, mongo_ids = ['user_id', 'boat_id'], neo_ids = ['operation_id'])
	#fill(entity_name = 'sensor_data', base = 'sensors_data', batch_size = 100, mongo_ids = ['sensor_id'])
	fill(entity_name = 'shift_state', base = 'shift_state', batch_size = 100, neo_ids = ['shift_id'])
	#fill(BOATS_COLLECTION_NAME, 'boats')

