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

CREATE_GET_X_SPEED_FUNCTION_QUERY = """
CREATE OR REPLACE FUNCTION {0}.get_x_speed (speed double, attack_angle double, direction_angle double) 
CALLED ON NULL INPUT 
RETURNS double LANGUAGE javascript AS
'speed * Math.cos(attack_angle) * Math.cos(direction_angle);';
"""

AVG_X_SPEED_QUERY = "select avg({0}.get_x_speed(speed, attack_angle, direction_angle)) from {0}.position;"

def get_avg_x_speed():

	#with UDF
	connection.execute(CREATE_GET_X_SPEED_FUNCTION_QUERY.format(DB_NAME))
	return list(connection.execute(AVG_X_SPEED_QUERY.format(DB_NAME)).current_rows[0].values())[0]

	#without UDF
	#return np.average([item.speed * math.cos(item.attack_angle) * math.cos(item.direction_angle) for item in Position.objects.all()])
	
	#in clickhouse
	#return Position.objects_in(db).aggregate(value = 'avg(speed * cos(atack_angle) * cos(direction_angle))')[0].value

def main():
	connection.setup([item.lstrip().rstrip() for item in DB_URLS.split(HOST_DELIMITER)], DB_NAME)
	print(get_avg_x_speed())

if __name__ == '__main__':
	main()