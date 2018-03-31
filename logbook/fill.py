import sys, os
import configparser

from cassandra.cqlengine import connection

sys.path.append('entities')

from position import Position
from system_test import SystemTest
from control_action import ControlAction
from sensor_data import SensorData
from shift_state import ShiftState

from data_adapters import get_positions
from data_adapters import get_system_tests
from data_adapters import get_control_actions
from data_adapters import get_sensors_data
from data_adapters import get_shift_states

config = configparser.ConfigParser()
config.read('../databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host'] 
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name'] 

POSITION_DATA_PATH = 'data/position.txt'
SYSTEM_TEST_DATA_PATH = 'data/system_test.txt'
CONTROL_ACTION_DATA_PATH = 'data/control_action.txt'
SENSOR_DATA_DATA_PATH = 'data/sensor_data.txt'
SHIFT_STATE_PATH = 'data/shift_state.txt'

def fill_position():
	for item in get_positions(POSITION_DATA_PATH):
		Position.create(time = item[0], x = item[1], y = item[2], z = item[3], speed = item[4], attack_angle = item[5], direction_angle = item[6])

def fill_system_test():
	for item in get_system_tests(SYSTEM_TEST_DATA_PATH):
		SystemTest.create(time = item[0], system_id = item[1], result = item[2])

def fill_control_action():
	for item in get_control_actions(CONTROL_ACTION_DATA_PATH):
		ControlAction.create(time = item[0], mac_address = item[1], user_id = item[2], command = item[3], params = item[4], result = item[5])

def fill_sensor_data():
	for item in get_sensors_data(SENSOR_DATA_DATA_PATH):
		SensorData.create(time = item[0], source_id = item[1], event = item[2], value_name = item[3], value = item[4], units = item[5])

def fill_shift_state():
	for item in get_shift_states(SHIFT_STATE_PATH):
		print(item)
		ShiftState.create(time = item[0], shift_id = item[1], warning_level = item[2], remaining_cartridges = item[3], \
			remaining_air = item[4], remaining_electricity = item[5], comment = item[6])

def main():
	connection.setup([DB_URL], DB_NAME)
	
	#fill_position()
	#fill_system_test()
	#fill_control_action()
	#fill_sensor_data()
	fill_shift_state()

if __name__ == '__main__':
	main()