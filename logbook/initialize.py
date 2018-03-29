import sys, os

from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import Memory

sys.path.append('entities')

from position import Position
from system_state import SystemState
from control_action import ControlAction
from sensor_data import SensorData

DB_URL = os.environ['DB_URL']
DB_NAME = os.environ['DB_NAME']

def main():
	db = Database(DB_NAME, db_url = DB_URL)

	db.create_table(Position)
	db.create_table(SystemState)
	db.create_table(ControlAction)
	db.create_table(SensorData)

if __name__ == '__main__':
	main()