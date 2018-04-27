import sys, os
import math
import configparser
import numpy as np
import operator

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/lobgook/entities')

from cassandra.cqlengine import connection

from position import Position
from system_test import SystemTest

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']
HOST_DELIMITER = os.environ.get('HOST_DELIMITER') if os.environ.get('HOST_DELIMITER') else config['CASSANDRA']['host_delimiter']
DB_URLS = os.environ.get('DB_URLS') if os.environ.get('DB_URLS') else config['CASSANDRA']['hosts']

def select(table_name, columns):
	columns_filter = ', '.join([item[0] for item in columns])
	values_filter = ' and '.join([\
		item[0] + ' = ' + str(item[1])\
		if isinstance(item[1], int) or isinstance(item[1], float) else\
		item[0] + ' = \'' + str(item[1]) + '\'' \
		for item in (item for item in columns if len(item) > 1)\
	])

	if len(values_filter) > 0:
		values_filter = 'where ' + values_filter
	print('select {2} from {0}.{1} {3} allow filtering;'.format(DB_NAME, table_name, columns_filter, values_filter))
	return connection.execute('select {2} from {0}.{1} {3} allow filtering;'.format(DB_NAME, table_name, columns_filter, values_filter)).current_rows

def get_system_tests():
	return connection.execute('select * from {0}.system_test;'.format(DB_NAME)).current_rows

def get_operation_states():
	return connection.execute('select * from {0}.operation_state;'.format(DB_NAME)).current_rows

def get_shift_states():
	return connection.execute('select * from {0}.shift_state;'.format(DB_NAME)).current_rows

def get_sensor_data():
	return connection.execute('select * from {0}.sensor_data;'.format(DB_NAME)).current_rows

def get_commands_by_user_id(user_id):
	return connection.execute('select * from {0}.control_action where user_id = 0x{1} ALLOW FILTERING;'.format(DB_NAME, user_id)).current_rows

def main():
	connection.setup([item.lstrip().rstrip() for item in DB_URLS.split(HOST_DELIMITER)], DB_NAME)

	table_name = sys.argv[1]
	columns = [column.split('=') for column in sys.argv[2:]]

	print(select(table_name, columns))

	#select('position', [['x', 10], ['y', 10], ['speed'], ['time']])

if __name__ == '__main__':
	main()