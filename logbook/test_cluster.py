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

DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']
HOST_DELIMITER = os.environ.get('HOST_DELIMITER') if os.environ.get('HOST_DELIMITER') else config['CASSANDRA']['host_delimiter']
DB_URLS = os.environ.get('DB_URLS') if os.environ.get('DB_URLS') else config['CASSANDRA']['hosts']

def main():

	try:
		connection.setup([item.lstrip().rstrip() for item in DB_URLS.split(HOST_DELIMITER)], DB_NAME)
	except:
		print('Connection is not set')
	else:
		print('Connection is set')

		try:
			connection.execute('select * from {0}.position;'.format(DB_NAME))
		except:
			print('Select query is not resolved')
		else:
			print('Select query is resolved')

if __name__ == '__main__':
	main()


