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

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host']
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

def get_average_x_speed():
	return np.average([item.speed * math.cos(item.attack_angle) * math.cos(item.direction_angle) for item in Position.objects.all()])
	#return Position.objects_in(db).aggregate(value = 'avg(speed * cos(atack_angle) * cos(direction_angle))')[0].value

def get_worst_system():
	marks = {}
	for item in SystemTest.objects.all():
		if marks.get(item.system_id.hex()):
			marks[item.system_id.hex()].append(item.result)
		else:
			marks[item.system_id.hex()] = [item.result]
	return sorted({item : np.average(marks[item]) for item in marks}.items(), key = operator.itemgetter(1))[0][0]
	#return SystemState.objects_in(db).filter(status = 'fail').aggregate('name', number_of_failures = 'count()').order_by('-number_of_failures')[0].name


def main():
	connection.setup([DB_URL], DB_NAME)

	print('average x speed is ', get_average_x_speed())
	print('the worst system is ', get_worst_system())


if __name__ == '__main__':
	main()