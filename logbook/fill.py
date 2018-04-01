import sys, os
import configparser

from cassandra.cqlengine import connection

sys.path.append('entities')

from position import Position
from system_test import SystemTest
from control_action import ControlAction
from sensor_data import SensorData
from shift_state import ShiftState
from operation_state import OperationState

from data_adapters import get_positions
from data_adapters import get_system_tests
from data_adapters import get_control_actions
from data_adapters import get_sensors_data
from data_adapters import get_shift_states
from data_adapters import get_operation_states

config = configparser.ConfigParser()
config.read('../databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host'] 
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name'] 

POSITION_DATA_PATH = 'data/position.txt'
SYSTEM_TEST_DATA_PATH = 'data/system_test.txt'
CONTROL_ACTION_DATA_PATH = 'data/control_action.txt'
SENSOR_DATA_DATA_PATH = 'data/sensor_data.txt'
SHIFT_STATE_PATH = 'data/shift_state.txt'
OPERATION_STATE_PATH = 'data/operation_state.txt'

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
		ShiftState.create(time = item[0], shift_id = item[1], warning_level = item[2], remaining_cartridges = item[3], \
			remaining_air = item[4], remaining_electricity = item[5], comment = item[6])

def fill_operation_state():
	for item in get_operation_states(OPERATION_STATE_PATH):
		OperationState.create(time = item[0], boat_id = item[1], operation_id = item[2], operation_status = item[3], \
			distance_to_the_ship = item[4], zenith = item[5], azimuth = item[6], hydrogenium = item[7], helium = item[8], \
			lithium = item[9], beryllium = item[10], borum = item[11], carboneum = item[12], nitrogenium = item[13], oxygenium = item[14], \
			fluorum = item[15], neon = item[16], natrium = item[17], magnesium = item[18], aluminium = item[19], silicium = item[20], \
			phosphorus = item[21], sulfur = item[22], chlorum = item[23], argon = item[24], kalium = item[25], calcium = item[26], \
			scandium = item[27], titanium = item[28], vanadium = item[29], chromium = item[30], manganum = item[31], ferrum = item[32], \
			cobaltum = item[33], niccolum = item[34], cuprum = item[35], zincum = item[36], gallium = item[37], germanium = item[38],\
			arsenicum = item[39], selenium = item[40], bromum = item[41], crypton = item[42], rubidium = item[43], strontium = item[44],\
			yttrium = item[45], zirconium = item[46], niobium = item[47], molybdaenum = item[48], technetium = item[49], ruthenium = item[50],\
			rhodium = item[51], palladium = item[52], argentum = item[53], cadmium = item[54], indium = item[55], stannum = item[56],\
			stibium = item[57], tellurium = item[58], iodium = item[59], xenon = item[60], caesium = item[61], barium = item[62],\
			lanthanum = item[63], cerium = item[64], praseodymium = item[65], neodymium = item[66], promethium = item[67], samarium = item[68],\
			europium = item[69], gadolinium = item[70], terbium = item[71], dysprosium = item[72], holmium = item[73], erbium = item[74],\
			thulium = item[75], ytterbium = item[76], lutetium = item[77], hafnium = item[78], tantalum = item[79], wolframium = item[80],\
			rhenium = item[81], osmium = item[82], iridium = item[83], platinum = item[84], aurum = item[85], hydrargyrum = item[86],\
			thallium = item[87], plumbum = item[88], bismuthum = item[89], polonium = item[90], astatum = item[91], radon = item[92],\
			francium = item[93], radium = item[94], actinium = item[95], thorium = item[96], protactinium = item[97], uranium = item[98],\
			neptunium = item[99], plutonium = item[100], americium = item[101], curium = item[102], berkelium = item[103], californium = item[104],\
			einsteinium = item[105], fermium = item[106], mendelevium = item[107], nobelium = item[108], lawrencium = item[109],\
			rutherfordium = item[110], dubnium = item[111], seaborgium = item[112], bohrium = item[113], hassium = item[114], meitnerium = item[115],\
			darmstadtium = item[116], roentgenium = item[117], copernicium = item[118], nihonium = item[119], flerovium = item[120], moscovium = item[121],\
			livermorium = item[122], tennessium = item[123], oganesson = item[124], comment = item[125])

def main():
	connection.setup([DB_URL], DB_NAME)
	
	#fill_position()
	#fill_system_test()
	#fill_control_action()
	#fill_sensor_data()
	fill_shift_state()
	#fill_operation_state()

if __name__ == '__main__':
	main()