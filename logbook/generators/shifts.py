from random import randint
from random import random
import os

import time
import datetime

WARNING_LEVELS = ['lowest', 'low', 'medium', 'heigh', 'highest']

DELIMITER = ' :: '

PERIOD = 3

def datetime_to_unix_time(datetime_to_convert):
	return time.mktime(datetime_to_convert.timetuple())

def generate_shift(time, shift_id, scale, probabilities_of_changing_level_up, probabilities_of_changing_level_down, filename):

	try:
		os.remove(filename)
	except OSError:
		pass

	log = open(filename,'a+')

	shift_length = randint(0, scale)

	max_decreasing_speed = 100 / (shift_length - 1)

	remaining_cartridges = 100
	remaining_air = 100
	remaining_electricity = 100

	current_level = 0

	shift_id_str = str(shift_id)

	for i in range(shift_length):

		comment = ''

		if random() < probabilities_of_changing_level_up[current_level]:
			current_level += 1
			remaining_cartridges -= random() * max_decreasing_speed * current_level
			comment = 'it is something strange'
		elif (random() < probabilities_of_changing_level_down[current_level]):
			current_level -= 1
			if current_level == 0:
				comment = 'the danger has gone'

		log.write(str(datetime_to_unix_time(time)) + DELIMITER + shift_id_str + DELIMITER + WARNING_LEVELS[current_level] + DELIMITER + str(remaining_cartridges) + \
		DELIMITER + str(remaining_air) + DELIMITER + str(remaining_electricity) + DELIMITER + comment + '\n')

		remaining_electricity -= random() * max_decreasing_speed
		remaining_air -= random() * max_decreasing_speed

		time += datetime.timedelta(0, PERIOD)

	log.close()