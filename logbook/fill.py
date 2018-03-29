import sys, os

from infi.clickhouse_orm.database import Database

sys.path.append('entities')

from position import Position
from system_state import SystemState
from control_action import ControlAction
from sensor_data import SensorData

from data_adapters import get_positions
from data_adapters import get_system_states
from data_adapters import get_control_actions
from data_adapters import get_sensors_data

DB_URL = os.environ['DB_URL']
DB_NAME = os.environ['DB_NAME']

POSITION_DATA_PATH = 'data/position.txt'
SYSTEM_STATE_DATA_PATH = 'data/system_state.txt'
CONTROL_ACTION_DATA_PATH = 'data/control_action.txt'
SENSOR_DATA_DATA_PATH = 'data/sensor_data.txt'

def fill_position(db):
	db.insert([Position(time = time, x = x, y = y, z = z, speed = speed, atack_angle = atack_angle, direction_angle = direction_angle) for \
	time, x, y, z, speed, atack_angle, direction_angle in get_positions(POSITION_DATA_PATH)])

def fill_system_state(db):
	db.insert([SystemState(time = time, name = name, id = id, status = status) for time, name, id, status in get_system_states(SYSTEM_STATE_DATA_PATH)])

def fill_control_action(db):
	db.insert([ControlAction(time = time, mac_address = mac_address, user = user, command = command, params = params, result = result) 
		for time, mac_address, user, command, params, result in get_control_actions(CONTROL_ACTION_DATA_PATH)])

def fill_sensor_data(db):
	db.insert([SensorData(time = time, source = source, location = location, event = event, value_name = value_name, value = value, units = units) 
		for time, source, location, event, value_name, value, units in get_sensors_data(SENSOR_DATA_DATA_PATH)])

def main():
	db = Database(DB_NAME, db_url = DB_URL)
	
	fill_position(db)
	fill_system_state(db)
	fill_control_action(db)
	fill_sensor_data(db)

if __name__ == '__main__':
	main()