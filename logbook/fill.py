import sys, os
import configparser
import datetime

import csv

from cassandra.cqlengine import connection

sys.path.append('entities')

from position import Position
from system_test import SystemTest
from control_action import ControlAction
from sensor_data import SensorData
from shift_state import ShiftState
from operation_state import OperationState

from data_adapters import string_to_bytes

config = configparser.ConfigParser()
config.read('../databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host'] 
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name'] 

POSITION_DATA_PATH = 'data/position.csv'
SYSTEM_TEST_DATA_PATH = 'data/system_test.csv'
CONTROL_ACTION_DATA_PATH = 'data/control_action.csv'
SENSOR_DATA_DATA_PATH = 'data/sensor_data.csv'
SHIFT_STATE_DATA_PATH = 'data/shift_state.csv'
OPERATION_STATE_DATA_PATH = 'data/operation_state.csv'

TIME_PATTERN = "%Y-%m-%d %H:%M:%S.%f"

def fill_position():

	with open(POSITION_DATA_PATH, newline='') as data:
		
		data_reader = csv.reader(data)

		for item in data_reader:
			Position.create(\
				date = datetime.datetime.strptime(item[0], TIME_PATTERN).date(),\
				time = datetime.datetime.strptime(item[0], TIME_PATTERN).time(),\
				x = float(item[1]),\
				y = float(item[2]),\
				z = float(item[3]),\
				speed = float(item[4]),\
				attack_angle = float(item[5]),\
				direction_angle = float(item[6]))

def fill_system_test():

	with open(SYSTEM_TEST_DATA_PATH, newline='') as data:
		
		data_reader = csv.reader(data)

		for item in data_reader:
			print(item[2])
			SystemTest.create(\
				date = datetime.datetime.strptime(item[0], TIME_PATTERN).date(),\
				time = datetime.datetime.strptime(item[0], TIME_PATTERN).time(),\
				system_id = string_to_bytes(item[1]),\
				result = int(float(item[2])))

def fill_control_action():

	with open(CONTROL_ACTION_DATA_PATH, newline='') as data:
		
		data_reader = csv.reader(data)

		for item in data_reader:
			ControlAction.create(\
				date = datetime.datetime.strptime(item[0], TIME_PATTERN).date(),\
				time = datetime.datetime.strptime(item[0], TIME_PATTERN).time(),\
				mac_address = string_to_bytes(item[1]),\
				user_id = string_to_bytes(item[2]),
				command = item[3],\
				params = item[4],\
				result = item[5]\
			)

def fill_sensor_data():

	with open(SENSOR_DATA_DATA_PATH, newline='') as data:
		
		data_reader = csv.reader(data)

		for item in data_reader:
			SensorData.create(\
				date = datetime.datetime.strptime(item[0], TIME_PATTERN).date(),\
				time = datetime.datetime.strptime(item[0], TIME_PATTERN).time(),\
				source_id = string_to_bytes(item[1]),\
				event = item[2],
				value_name = item[3],\
				value = float(item[4]),\
				units = item[5]\
			)

def fill_shift_state():

	with open(SHIFT_STATE_DATA_PATH, newline='') as data:
		
		data_reader = csv.reader(data)

		for item in data_reader:
			ShiftState.create(\
				date = datetime.datetime.strptime(item[0], TIME_PATTERN).date(),\
				time = datetime.datetime.strptime(item[0], TIME_PATTERN).time(),\
				shift_id = string_to_bytes(item[1]),\
				warning_level = item[2],
				remaining_cartridges = int(float(item[3])),\
				remaining_air = int(float(item[4])),\
				remaining_electricity = int(float(item[5])),\
				comment = item[6]\
			)

def fill_operation_state():

	with open(OPERATION_STATE_DATA_PATH, newline='') as data:
		
		data_reader = csv.reader(data)

		for item in data_reader:
			OperationState.create(\
				date = datetime.datetime.strptime(item[0], TIME_PATTERN).date(),\
				time = datetime.datetime.strptime(item[0], TIME_PATTERN).time(),\
				boat_id = string_to_bytes(item[1]),\
				operation_id = string_to_bytes(item[2]),\
				operation_status = item[3],\
				distance_to_the_ship = float(item[4]),\
				zenith = float(item[5]),\
				azimuth = float(item[6]),\

				hydrogenium = float(item[7]),\
				helium = float(item[8]),\
				lithium = float(item[9]),\
				beryllium = float(item[10]),\
				borum = float(item[11]),\
				carboneum = float(item[12]),\
				nitrogenium = float(item[13]),\
				oxygenium = float(item[14]),\
				fluorum = float(item[15]),\
				neon = float(item[16]),\
				natrium = float(item[17]),\
				magnesium = float(item[18]),\
				aluminium = float(item[19]),\
				silicium = float(item[20]),\
				phosphorus = float(item[21]),\
				sulfur = float(item[22]),\
				chlorum = float(item[23]),\
				argon = float(item[24]),\
				kalium = float(item[25]),\
				calcium = float(item[26]),\
				scandium = float(item[27]),\
				titanium = float(item[28]),\
				vanadium = float(item[29]),\
				chromium = float(item[30]),\
				manganum = float(item[31]),\
				ferrum = float(item[32]),\
				cobaltum = float(item[33]),\
				niccolum = float(item[34]),\
				cuprum = float(item[35]),\
				zincum = float(item[36]),\
				gallium = float(item[37]),\
				germanium = float(item[38]),\
				arsenicum = float(item[39]),\
				selenium = float(item[40]),\
				bromum = float(item[41]),\
				crypton = float(item[42]),\
				rubidium = float(item[43]),\
				strontium = float(item[44]),\
				yttrium = float(item[45]),\
				zirconium = float(item[46]),\
				niobium = float(item[47]),\
				molybdaenum = float(item[48]),\
				technetium = float(item[49]),\
				ruthenium = float(item[50]),\
				rhodium = float(item[51]),\
				palladium = float(item[52]),\
				argentum = float(item[53]),\
				cadmium = float(item[54]),\
				indium = float(item[55]),\
				stannum = float(item[56]),\
				stibium = float(item[57]),\
				tellurium = float(item[58]),\
				iodium = float(item[59]),\
				xenon = float(item[60]),\
				caesium = float(item[61]),\
				barium = float(item[62]),\
				lanthanum = float(item[63]),\
				cerium = float(item[64]),\
				praseodymium = float(item[65]),\
				neodymium = float(item[66]),\
				promethium = float(item[67]),\
				samarium = float(item[68]),\
				europium = float(item[69]),\
				gadolinium = float(item[70]),\
				terbium = float(item[71]),\
				dysprosium = float(item[72]),\
				holmium = float(item[73]),\
				erbium = float(item[74]),\
				thulium = float(item[75]),\
				ytterbium = float(item[76]),\
				lutetium = float(item[77]),\
				hafnium = float(item[78]),\
				tantalum = float(item[79]),\
				wolframium = float(item[80]),\
				rhenium = float(item[81]),\
				osmium = float(item[82]),\
				iridium = float(item[83]),\
				platinum = float(item[84]),\
				aurum = float(item[85]),\
				hydrargyrum = float(item[86]),\
				thallium = float(item[87]),\
				plumbum = float(item[88]),\
				bismuthum = float(item[89]),\
				polonium = float(item[90]),\
				astatum = float(item[91]),\
				radon = float(item[92]),\
				francium = float(item[93]),\
				radium = float(item[94]),\
				actinium = float(item[95]),\
				thorium = float(item[96]),\
				protactinium = float(item[97]),\
				uranium = float(item[98]),\
				neptunium = float(item[99]),\
				plutonium = float(item[100]),\
				americium = float(item[101]),\
				curium = float(item[102]),\
				berkelium = float(item[103]),\
				californium = float(item[104]),\
				einsteinium = float(item[105]),\
				fermium = float(item[106]),\
				mendelevium = float(item[107]),\
				nobelium = float(item[108]),\
				lawrencium = float(item[109]),\
				rutherfordium = float(item[110]),\
				dubnium = float(item[111]),\
				seaborgium = float(item[112]),\
				bohrium = float(item[113]),\
				hassium = float(item[114]),\
				meitnerium = float(item[115]),\
				darmstadtium = float(item[116]),\
				roentgenium = float(item[117]),\
				copernicium = float(item[118]),\
				nihonium = float(item[119]),\
				flerovium = float(item[120]),\
				moscovium = float(item[121]),\
				livermorium = float(item[122]),\
				tennessium = float(item[123]),\
				oganesson = float(item[124]),\

				comment = item[125]\
			)

def main():
	connection.setup([DB_URL], DB_NAME)
	
	#fill_position()
	fill_system_test()
	fill_control_action()
	fill_sensor_data()
	fill_shift_state()
	fill_operation_state()

if __name__ == '__main__':
	main()