import sys, os
import configparser

from cassandra.cqlengine import connection

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/')

config = configparser.ConfigParser()
config.read('../databases.config')

HOST_DELIMITER = os.environ.get('HOST_DELIMITER') if os.environ.get('HOST_DELIMITER') else config['CASSANDRA']['host_delimiter']
DB_URLS = os.environ.get('DB_URLS') if os.environ.get('DB_URLS') else config['CASSANDRA']['hosts']
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

def setup_connection():
	urls = DB_URLS.split(HOST_DELIMITER)
	for i in range(len(urls)):
		connection.setup([DB_URL], DB_NAME)