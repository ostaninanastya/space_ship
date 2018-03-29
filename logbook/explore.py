import sys, os
import math

sys.path.append('entities')

from infi.clickhouse_orm.database import Database

from position import Position
from system_state import SystemState

DB_URL = os.environ['DB_URL']
DB_NAME = os.environ['DB_NAME']

def get_average_x_speed(db):
	return Position.objects_in(db).aggregate(value = 'avg(speed * cos(atack_angle) * cos(direction_angle))')[0].value

def get_worst_system(db):
	return SystemState.objects_in(db).filter(status = 'fail').aggregate('name', number_of_failures = 'count()').order_by('-number_of_failures')[0].name


def main():
	db = Database(DB_NAME, db_url = DB_URL)

	print('average x speed is ', get_average_x_speed(db))
	print('the worst system is ', get_worst_system(db))


if __name__ == '__main__':
	main()