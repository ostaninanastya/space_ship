import sys, os
import math
import configparser
import numpy as np
import operator

sys.path.append('entities')

from cassandra.cqlengine import connection

from position import Position
from system_test import SystemTest

config = configparser.ConfigParser()
config.read('../databases.config')

DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']
HOST_DELIMITER = os.environ.get('HOST_DELIMITER') if os.environ.get('HOST_DELIMITER') else config['CASSANDRA']['host_delimiter']
DB_URLS = os.environ.get('DB_URLS') if os.environ.get('DB_URLS') else config['CASSANDRA']['hosts']


def update(table_name, columns_getter, columns_setter):
	columns_filter = ', '.join([item[0] for item in columns_getter])
	
	values_filter = ' and '.join([\
		item[0] + ' = ' + str(item[1])\
		if isinstance(item[1], int) or isinstance(item[1], float) else\
		item[0] + ' = \'' + str(item[1]) + '\'' \
		for item in (item for item in columns_getter if len(item) > 1)\
	])

	for column in columns_setter:
		if len(column) > 1:
			try:
				column[1] = int(column[1])
			except ValueError:
				try:
					column[1] = float(column[1])
				except ValueError:
					pass

	values_setter = ', '.join([\
		item[0] + ' = ' + str(item[1])\
		if isinstance(item[1], int) or isinstance(item[1], float) else\
		item[0] + ' = \'' + str(item[1]) + '\'' \
		for item in (item for item in columns_setter if len(item) > 1)\
	])

	if len(values_filter) > 0:
		values_filter = 'where ' + values_filter
	
	if len(values_setter) > 0:
		values_setter = 'set ' + values_setter

	print('update {0}.{1} {2} {3} allow filtering;'.format(DB_NAME, table_name, values_filter, values_setter))
	return connection.execute('update {0}.{1} {3} {2};'.format(DB_NAME, table_name, values_filter, values_setter)).current_rows

def main():
	connection.setup([item.lstrip().rstrip() for item in DB_URLS.split(HOST_DELIMITER)], DB_NAME)

	table_name = sys.argv[1]
	columns_getter = [column.split('=') for column in (item for item in sys.argv[2:] if item.find('->') < 0)]
	columns_setter = [column.split('->') for column in (item for item in sys.argv[2:] if item.find('=') < 0)]

	print(update(table_name, columns_getter, columns_setter))

if __name__ == '__main__':
	main()