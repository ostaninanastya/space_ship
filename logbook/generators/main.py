from random import random
from random import randint
from random import shuffle
import math
import datetime
import time
import os, sys

import csv

from operations import generate_prometheus_operation
from operations import get_outer_area_composition
from shifts import generate_shift

sys.path.append('adapters')

import mongo_adapter
import neo4j_adapter

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data_adapters import get_strings

#print(mongo_adapter.get_all_ids('boat_test')[0])

DELIMITER = ' :: '

SHIFT_STATE_DATA_PATH = 'data/shift_state.csv'
OPERATION_STATE_DATA_PATH = 'data/operation_state.csv'

#position

POSITION_DATA_PATH = 'data/position.csv'

PERIOD = 3
COMMAND_DELAY = 1
REQUEST_DELAY = 2

#command

COMMAND_DATA_PATH = 'data/control_action.csv'

ROOT_MAC_ADDRESS = 'ACB57DF96885'
ROOT_USER = mongo_adapter.get_all_ids('user_test')[0]

PROBABILITY_OF_CHANGING_DIRECTION = 0.2
PROBABILITY_OF_REQUESTING_VALUE = 0.2

#system_state

SYSTEM_STATE_DATA_PATH = 'data/system_test.csv'

SYSTEM_NAMES = ['fuel system', 'main engine', 'spare engine', 'main thrusters', 'spare thrusters', 'power system']
SYSTEM_INDEXES = mongo_adapter.get_all_ids('system_test')
SYSTEM_STATES = ['working', 'fail', 'being_fixed', 'testing']
SYSTEM_PROBABILITIES = [[0.2, 0.5, 0.8, 0.95], \
						[0.4, 0.2, 0.8, 0.95], \
						[0.3, 0.2, 0.8, 0.95], \
						[0.3, 0.2, 0.8, 0.95], \
						[0.3, 0.2, 0.8, 0.95], \
						[0.3, 0.2, 0.8, 0.95]]
SYSTEM_CURRENT_STATES = [0, 0, 0, 0, 0, 0]

#sensor_data

SENSOR_DATA_DATA_PATH = 'data/sensor_data.csv'

#SENSORS = ['MINAS_MORGUL T400', 'STADDLE N23', 'VALMAR 17']
SENSORS = mongo_adapter.get_all_ids('source_test')
LOCATIONS = ['top_edge', 'left_side', 'laboratory']

VALUE_TYPES = get_strings('enums/value_types')
VALUE_UNITS = get_strings('enums/units')
VALUE_RANDOM_KOEFFICIENTS = [12, 100, 24, 100]

def try_switch_system_state(id):
	if random() < SYSTEM_PROBABILITIES[id][SYSTEM_CURRENT_STATES[id]]:
		SYSTEM_CURRENT_STATES[id] += 1
		if (SYSTEM_CURRENT_STATES[id] >= len(SYSTEM_STATES)):
			SYSTEM_CURRENT_STATES[id] = 0

def datetime_to_unix_time(datetime_to_convert):
	return time.mktime(datetime_to_convert.timetuple())

def get_command_params(attack_angle, direction_angle):

	result = ''

	if (attack_angle > 0):
		result += 'up'
	else:
		result += 'down'

	result += ' '

	if (direction_angle > 0):
		result += 'left'
	else:
		result += 'right'

	return result

def generate(number_of_values):

	for filename in [POSITION_DATA_PATH, COMMAND_DATA_PATH, SYSTEM_STATE_DATA_PATH, SENSOR_DATA_DATA_PATH]:
		try:
			os.remove(filename)
		except OSError:
			pass

	position_log = open(POSITION_DATA_PATH, 'w', newline='')
	command_log = open(COMMAND_DATA_PATH, 'w', newline='')
	system_state_log = open(SYSTEM_STATE_DATA_PATH, 'w', newline='')
	sensor_data_log = open(SENSOR_DATA_DATA_PATH, 'w', newline='')

	position_log_writer = csv.writer(position_log, quoting=csv.QUOTE_MINIMAL)
	command_log_writer = csv.writer(command_log, quoting=csv.QUOTE_MINIMAL)
	system_state_log_writer = csv.writer(system_state_log, quoting=csv.QUOTE_MINIMAL)
	sensor_data_log_writer = csv.writer(sensor_data_log, quoting=csv.QUOTE_MINIMAL)

	x = 0
	y = 0
	z = 0

	v = 10
	attack_angle = 0
	direction_angle = 0

	time = datetime.datetime.now()

	for i in range(number_of_values):
		
		position_log_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S.%f"), x, y, z, v, attack_angle, direction_angle])

		z += v * math.sin(attack_angle)
		x += v * math.cos(attack_angle) * math.cos(direction_angle)
		y += v * math.sin(direction_angle)

		time += datetime.timedelta(0, PERIOD)

		if (random() < PROBABILITY_OF_REQUESTING_VALUE):

			sensor_id = randint(0, len(SENSORS) - 1)

			value_id = randint(0, len(VALUE_TYPES) - 1)

			command_log_writer.writerow([datetime.datetime.fromtimestamp(datetime_to_unix_time(time) - REQUEST_DELAY).strftime("%Y-%m-%d %H:%M:%S.%f"),\
				ROOT_MAC_ADDRESS, ROOT_USER, 'get', '--sensor=' + SENSORS[sensor_id] + ' ' + '--value_name=' + VALUE_TYPES[value_id], \
				str(random() * VALUE_RANDOM_KOEFFICIENTS[value_id]) + ' ' + VALUE_UNITS[value_id]])

			sensor_data_log_writer.writerow([datetime.datetime.fromtimestamp(datetime_to_unix_time(time) - REQUEST_DELAY).strftime("%Y-%m-%d %H:%M:%S.%f"), SENSORS[sensor_id], \
				'request', VALUE_TYPES[value_id], (random() * VALUE_RANDOM_KOEFFICIENTS[value_id]), VALUE_UNITS[value_id]])


		if (random() < PROBABILITY_OF_CHANGING_DIRECTION):

			attack_angle_delta = (random() - 0.5)
			direction_angle_delta = (random() - 0.5)

			command_log_writer.writerow([datetime.datetime.fromtimestamp(datetime_to_unix_time(time) - COMMAND_DELAY).strftime("%Y-%m-%d %H:%M:%S.%f"), ROOT_MAC_ADDRESS,\
				ROOT_USER, 'go', get_command_params(attack_angle_delta, direction_angle_delta), 'ok'])

			for i in range(len(SYSTEM_INDEXES)):
				system_state_log_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S.%f"), SYSTEM_INDEXES[i], (random() * 50 + 50)])
				#try_switch_system_state(i)

			for i in range(len(VALUE_TYPES)):
				for j in range(len(SENSORS)):
					sensor_data_log_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S.%f"), SENSORS[j], 'timeout', VALUE_TYPES[i], (random() * VALUE_RANDOM_KOEFFICIENTS[i]), VALUE_UNITS[i]])

			attack_angle += attack_angle_delta
			direction_angle += direction_angle_delta

	position_log.close()
	command_log.close()
	system_state_log.close()
	sensor_data_log.close()

def main():
	pass
	#generate_shift(datetime.datetime.now(), neo4j_adapter.get_all_ids('Shift')[0], 50, [0.2, 0.3, 0.3, 0.3, 0], [0, 0.5, 0.6, 0.4, 0.4], SHIFT_STATE_DATA_PATH)
	#generate(50)
	generate_prometheus_operation(50, datetime.datetime.now(), mongo_adapter.get_all_ids('boat_test')[0], neo4j_adapter.get_all_ids('Operation')[0], get_outer_area_composition(118, None, None), OPERATION_STATE_DATA_PATH)
	#initial = get_outer_area_composition(118, None, None)
	#print(stringify_area_composition(initial))
	#print(stringify_area_composition(get_outer_area_composition(118, initial, 1)))

if __name__ == '__main__':
	main()