from random import random
from random import randint
import math
import datetime
import time
import os

DELIMITER = ' :: '

#position

POSITION_DATA_PATH = '../data/position.txt'

PERIOD = 3
COMMAND_DELAY = 1
REQUEST_DELAY = 2

#command

COMMAND_DATA_PATH = '../data/control_action.txt'

ROOT_MAC_ADDRESS = 'AC:B5:7D:F9:68:85'
ROOT_USER = 'commander'

PROBABILITY_OF_CHANGING_DIRECTION = 0.2
PROBABILITY_OF_REQUESTING_VALUE = 0.2

#system_state

SYSTEM_STATE_DATA_PATH = '../data/system_state.txt'

SYSTEM_NAMES = ['fuel system', 'main engine', 'spare engine', 'main thrusters', 'spare thrusters', 'power system']
SYSTEM_INDEXES = [0, 1, 2, 4, 5, 8]
SYSTEM_STATES = ['working', 'fail', 'being_fixed', 'testing']
SYSTEM_PROBABILITIES = [[0.2, 0.5, 0.8, 0.95], \
						[0.4, 0.2, 0.8, 0.95], \
						[0.3, 0.2, 0.8, 0.95], \
						[0.3, 0.2, 0.8, 0.95], \
						[0.3, 0.2, 0.8, 0.95], \
						[0.3, 0.2, 0.8, 0.95]]
SYSTEM_CURRENT_STATES = [0, 0, 0, 0, 0, 0]

#sensor_data

SENSOR_DATA_DATA_PATH = '../data/sensor_data.txt'

SENSORS = ['MINAS_MORGUL T400', 'STADDLE N23', 'VALMAR 17']
LOCATIONS = ['top_edge', 'left_side', 'laboratory']

VALUE_TYPES = ['cold_dark_matter_concentration', 'hot_dark_matter_concentration', 'warm_dark_matter_concentration', 'space_radiation']
VALUE_UNITS = ['CeV', 'TeV', 'eV', 'keV']
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

	position_log = open(POSITION_DATA_PATH,'a+')
	command_log = open(COMMAND_DATA_PATH,'a+')
	system_state_log = open(SYSTEM_STATE_DATA_PATH,'a+')
	sensor_data_log = open(SENSOR_DATA_DATA_PATH,'a+')

	x = 0
	y = 0
	z = 0

	v = 10
	attack_angle = 0
	direction_angle = 0

	time = datetime.datetime.now()

	for i in range(number_of_values):
		
		position_log.write(str(datetime_to_unix_time(time)) + DELIMITER + str(x) + DELIMITER + str(y) + \
			DELIMITER + str(z) + DELIMITER + str(v) + DELIMITER + str(attack_angle) + DELIMITER + str(direction_angle) + '\n')

		z += v * math.sin(attack_angle)
		x += v * math.cos(attack_angle) * math.cos(direction_angle)
		y += v * math.sin(direction_angle)

		time += datetime.timedelta(0, PERIOD)

		if (random() < PROBABILITY_OF_REQUESTING_VALUE):

			sensor_id = randint(0, len(SENSORS) - 1)

			value_id = randint(0, len(VALUE_TYPES) - 1)

			command_log.write(str(datetime_to_unix_time(time) - REQUEST_DELAY) + DELIMITER + ROOT_MAC_ADDRESS + DELIMITER + ROOT_USER + DELIMITER + 'get' + \
				DELIMITER + '--sensor=' + SENSORS[sensor_id] + ' ' + '--value_name=' + VALUE_TYPES[value_id] + DELIMITER + \
				str(random() * VALUE_RANDOM_KOEFFICIENTS[value_id]) + ' ' + VALUE_UNITS[value_id] + '\n')

			sensor_data_log.write(str(datetime_to_unix_time(time) - REQUEST_DELAY) + DELIMITER + SENSORS[sensor_id] + DELIMITER + \
				LOCATIONS[sensor_id] + DELIMITER + 'request' + DELIMITER + VALUE_TYPES[value_id] + DELIMITER + \
				str(random() * VALUE_RANDOM_KOEFFICIENTS[value_id]) + DELIMITER + VALUE_UNITS[value_id] + '\n')


		if (random() < PROBABILITY_OF_CHANGING_DIRECTION):

			attack_angle_delta = (random() - 0.5)
			direction_angle_delta = (random() - 0.5)

			command_log.write(str(datetime_to_unix_time(time) - COMMAND_DELAY) + DELIMITER + ROOT_MAC_ADDRESS + DELIMITER + ROOT_USER + DELIMITER + 'go' + \
				DELIMITER + get_command_params(attack_angle_delta, direction_angle_delta) + DELIMITER + 'ok' + '\n')

			for i in range(len(SYSTEM_INDEXES)):
				system_state_log.write(str(datetime_to_unix_time(time)) + DELIMITER + SYSTEM_NAMES[i] + DELIMITER + str(SYSTEM_INDEXES[i]) + \
					DELIMITER + SYSTEM_STATES[SYSTEM_CURRENT_STATES[i]] + '\n')
				try_switch_system_state(i)

			for i in range(len(VALUE_TYPES)):
				for j in range(len(SENSORS)):
					sensor_data_log.write(str(datetime_to_unix_time(time)) + DELIMITER + SENSORS[j] + DELIMITER + LOCATIONS[j] + DELIMITER + 'timeout' + \
					DELIMITER + VALUE_TYPES[i] + DELIMITER + str(random() * VALUE_RANDOM_KOEFFICIENTS[i]) + DELIMITER + VALUE_UNITS[i] + '\n')

			attack_angle += attack_angle_delta
			direction_angle += direction_angle_delta

	position_log.close()
	command_log.close()
	system_state_log.close()
	sensor_data_log.close()


def main():
	generate(50)

if __name__ == '__main__':
	main()