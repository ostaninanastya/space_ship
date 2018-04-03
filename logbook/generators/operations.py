from random import random
from random import randint
from random import shuffle

import os

import csv

import datetime
import time

DELIMITER = ' :: '

PERIOD = 3

OPERATION_STATUSES = ['getting_ready', 'detaching_from_ship', 'going_to_the_place_of_operation', 'operating', 'returning', 'attaching_to_ship', 'finishing']

GETTING_READY_COMMENTS = ['started', 'instructions are given', 'systems checked', 'testing finished']
DETACHING_FROM_SHIP_COMMENTS = ['started', 'energy system started', 'undocking finished']
GOING_COMMENTS = ['started', 'second engine started', 'object is visible', 'convergence started']
OPERATING_COMMENTS = ['started', 'found stone cylinders', 'taking a cylinder from the structure', 'storm started, returning to the boat']
RETURNING_COMMENTS = ['started', 'investigating the cylinder and the liquid inside', 'making panic', 'third engine started']
ATTACHING_TO_SHIP_COMMENTS = ['started', 'docking started', 'energy system stopped']
FINISHING_COMMENTS = ['started', 'systems stopped', 'data loaded']

def datetime_to_unix_time(datetime_to_convert):
	return time.mktime(datetime_to_convert.timetuple())

def get_randint(low, heigh):
	try:
		return randint(low, heigh)
	except:
		return heigh

def stringify_area_composition(area_composition):

	result = ''

	for i in range(len(area_composition)):
		result += str(area_composition[i])

		if i < len(area_composition) - 1:
			result += DELIMITER

	return result


def get_outer_area_composition(number_of_values, initial, speed):
	
	result = []

	'''if not initial:'''

	for i in range(number_of_values - 1):
		result.append(random() * (100 - sum(result)))

	result.append(100 - sum(result))

	shuffle(result)

	'''else:

		for item in initial:

			item_random_increasing = random() * speed - speed/2

			if item + item_random_increasing < 0:
				item_increasing = - item

			else if item + item_random_increasing > 100:
				item_increasing = 100 - item

			else:

				item_increasing = item_random_increasing



			item_increasing = item_random_increasing if item + item_random_increasing > 0

			new_item = item + (random() * speed - speed/2)

			result.append(new_item if new_item >= 0 else 0)'''

	return result

def generate_prometheus_operation(scale, time, boat_id, operation_id, initial_area_composition, filename):

	try:
		os.remove(filename)
	except OSError:
		pass

	log = open(filename,'w', newline='')

	log_writer = csv.writer(log, quoting=csv.QUOTE_MINIMAL)

	boat_id_str = str(boat_id)
	operation_id_str = str(operation_id)

	distance_to_the_ship = 0
	angle = 0
	second_angle = 0

	comments = [GETTING_READY_COMMENTS, DETACHING_FROM_SHIP_COMMENTS, GOING_COMMENTS, OPERATING_COMMENTS, \
		RETURNING_COMMENTS, ATTACHING_TO_SHIP_COMMENTS, FINISHING_COMMENTS]
	
	scale_koefficients = [0.6, 0.8, 0.6, 0.5, 0.6, 0.8, 0.4, 0.2]
	distance_speed_max = [0, 2, 10, 0, -1, -2, 0]
	angle_speed_max = [0, 0, 10, 2, -1, -2, 0]
	outer_area_speed = [0.5, 5, 10, 2, 10, 5, 0]

	for j in range(len(comments)):

		stage_length = get_randint(0, int(scale * scale_koefficients[j]))

		distance_step_to_return = distance_to_the_ship / stage_length
		angle_step_to_return = angle / stage_length
		second_angle_step_to_return = second_angle / stage_length

		comments_time = [0]

		for i in range(1, len(comments[j])):
			comments_time.append(get_randint(comments_time[i - 1] + 1, stage_length))

		for i in range(stage_length):
			comment = ''

			if i in comments_time:
				comment = comments[j][comments_time.index(i)]

			log_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S.%f"), boat_id_str, operation_id_str, OPERATION_STATUSES[j], \
				distance_to_the_ship, angle, second_angle] + initial_area_composition + [comment])

			initial_area_composition = get_outer_area_composition(118, initial_area_composition, outer_area_speed[j])

			time += datetime.timedelta(0, PERIOD)

			if distance_speed_max[j] >= 0:
				
				distance_to_the_ship += (random() * distance_speed_max[j] - distance_speed_max[j]/2)
				angle += (random() * angle_speed_max[j] - angle_speed_max[j]/2)
				second_angle += (random() * angle_speed_max[j] - angle_speed_max[j]/2)

			else:
				distance_to_the_ship -= distance_step_to_return
				angle -= angle_step_to_return
				second_angle -= second_angle_step_to_return

		if distance_speed_max[j] == -2:
			
			distance_to_the_ship = 0
			angle = 0
			second_angle = 0

	log.close()