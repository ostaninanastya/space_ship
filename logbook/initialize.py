import sys, os
import configparser
import datetime
import re

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra import cqlengine

sys.path.append('entities')

from system_test import SystemTest
from control_action import ControlAction
from position import Position
from sensor_data import SensorData
from shift_state import ShiftState
from operation_state import OperationState

config = configparser.ConfigParser()
config.read('../databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host']
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

def main():
	connection.setup([DB_URL], DB_NAME)
	
	sync_table(SystemTest)
	sync_table(ControlAction)
	sync_table(Position)
	sync_table(SensorData)
	sync_table(ShiftState)
	sync_table(OperationState)

if __name__ == '__main__':
	main()

