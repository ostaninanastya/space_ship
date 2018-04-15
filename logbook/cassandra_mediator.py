import sys, os
import configparser
import datetime
from collections import namedtuple
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
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host'] 
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

connection.setup([DB_URL], DB_NAME)

#

def remove(timestamp, entity_name, dicted = False):
	deleted = connection.execute("select * from {0}.{3} where date='{1}' and time='{2}';"\
	.format(DB_NAME, timestamp.strftime(DATE_PATTERN), timestamp.strftime(TIME_PATTERN), entity_name))[0]

	connection.execute("delete from {0}.{3} where date='{1}' and time='{2}';"\
	.format(DB_NAME, timestamp.strftime(DATE_PATTERN), timestamp.strftime(TIME_PATTERN), entity_name))
	
	if not dicted:
		return namedtuple('Struct', deleted.keys())(*deleted.values())
	return deleted
#

def create_position(timestamp, x, y, z, speed, attack_angle, direction_angle):
	return Position.create(date = timestamp.date(), time = timestamp.time(), x = x, y = y, z = z,\
		                   speed = speed, attack_angle = attack_angle, direction_angle = direction_angle)

def remove_position(timestamp):
	return remove(timestamp, 'position')

#

def create_control_action(timestamp, mac_address, user_id, command, params, result):
	return ControlAction.create(\
			date = timestamp.date(), time = timestamp.time(), mac_address = string_to_bytes(mac_address), user_id = string_to_bytes(user_id),
			command = command, params = params, result = result)

def remove_control_action(timestamp):
	return remove(timestamp, 'control_action')

#/api/create/controlaction/fields=ok&where=timestamp:'2017-02-12 23:59:59',mac:'acb57df96885',user:'5ac8a57c1767171855a9dd8d',command:'find',params:'smth',result:'smth'
#/api/remove/controlaction/fields=ok&where=timestamp:'2017-02-12 23:59:59'

#

def create_system_test(timestamp, system_id, result):
	return SystemTest.create(date = timestamp.date(), time = timestamp.time(), system_id = string_to_bytes(system_id), result = result)

def remove_system_test(timestamp):
	return remove(timestamp, 'system_test', dicted = True)

#/api/create/systemtest/fields=ok&where=timestamp:'2017-02-12 23:59:59',system:'5abfcb1aa75ef28692553915',result:69
#/api/remove/systemtest/fields=ok&where=timestamp:'2017-02-12 23:59:59'


def create_sensor_data(timestamp, source, event, meaning, value, units):
	return SensorData.create(\
				date = timestamp.date(), time = timestamp.time(), source_id = string_to_bytes(source), event = event, value_name = meaning,\
				value = value, units = units)

def remove_sensor_data(timestamp):
	return remove(timestamp, 'sensor_data', dicted = True)

#/api/create/sensordata/fields=ok&where=timestamp:'2017-02-12 23:59:59',source:'5ad21f46d678f464107e6d63',event:'timeout',meaning:'space_radiation',value:13.17,units:'eV'
#/api/remove/sensordata/fields=ok&where=timestamp:'2017-02-12 23:59:59'

def create_shift_state(timestamp, shift_id, warning_level, remaining_cartridges, remaining_air, remaining_electricity, comment):
	return ShiftState.create(\
				date = timestamp.date(), time = timestamp.time(), shift_id = string_to_bytes(shift_id),\
				warning_level = warning_level, remaining_cartridges = remaining_cartridges, remaining_air = remaining_air,\
				remaining_electricity = remaining_electricity, comment = comment)

def remove_shift_state(timestamp):
	return remove(timestamp, 'shift_state', dicted = True)

#/api/create/shiftstate/fields=ok&where=timestamp:'2017-02-12 23:59:59',shift:'1d16608544224e24b6b986f1b1390101',warninglevel:'medium',remainingcartridges:69,remainingelectricity:69,remainingair:69,comment:'THERE IS A BALROG!!!'
#/api/remove/shiftstate/fields=ok&where=timestamp:'2017-02-12 23:59:59'

def create_operation_state(timestamp, boat_id, operation_id, operation_status, distance_to_the_ship, zenith, azimuth,\
 	hydrogenium, helium, lithium, beryllium, borum,\
    carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,\
    scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,\
    crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,\
    stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,\
    terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,\
    hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,\
    plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,\
    seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,\
    oganesson, comment):
	return OperationState.create(date = timestamp.date(), time = timestamp.time(), boat_id = string_to_bytes(boat_id) if boat_id != '' else None, 
			operation_id = string_to_bytes(operation_id), operation_status = operation_status, distance_to_the_ship = distance_to_the_ship,\
			zenith = zenith, azimuth = azimuth, hydrogenium = hydrogenium, helium = helium, lithium = lithium, beryllium = beryllium,\
			borum = borum, carboneum = carboneum, nitrogenium = nitrogenium, oxygenium = oxygenium, fluorum = fluorum, neon = neon,\
			natrium = natrium, magnesium = magnesium, aluminium = aluminium, silicium = silicium, phosphorus = phosphorus, sulfur = sulfur,\
			chlorum = chlorum, argon = argon, kalium = kalium, calcium = calcium, scandium = scandium, titanium = titanium, vanadium = vanadium,\
			chromium = chromium, manganum = manganum, ferrum = ferrum, cobaltum = cobaltum, niccolum = niccolum, cuprum = cuprum, zincum = zincum,\
			gallium = gallium, germanium = germanium, arsenicum = arsenicum, selenium = selenium, bromum = bromum, crypton = crypton,\
			rubidium = rubidium, strontium = strontium, yttrium = yttrium, zirconium = zirconium, niobium = niobium, molybdaenum = molybdaenum,\
		 	technetium = technetium, ruthenium = ruthenium, rhodium = rhodium, palladium = palladium, argentum = argentum, cadmium = cadmium,\
		 	indium = indium, stannum = stannum, stibium = stibium, tellurium = tellurium, iodium = iodium, xenon = xenon, caesium = caesium,\
		 	barium = barium, lanthanum = lanthanum, cerium = cerium, praseodymium = praseodymium, neodymium = neodymium, promethium = promethium,\
		 	samarium = samarium, europium = europium, gadolinium = gadolinium, terbium = terbium, dysprosium = dysprosium, holmium = holmium,\
		 	erbium = erbium, thulium = thulium, ytterbium = ytterbium, lutetium = lutetium, hafnium = hafnium, tantalum = tantalum,\
		 	wolframium = wolframium, rhenium = rhenium, osmium = osmium, iridium = iridium, platinum = platinum, aurum = aurum, hydrargyrum = hydrargyrum,\
		 	thallium = thallium, plumbum = plumbum, bismuthum = bismuthum, polonium = polonium, astatum = astatum, radon = radon,\
		 	francium = francium, radium = radium, actinium = actinium, thorium = thorium, protactinium = protactinium, uranium = uranium,\
		 	neptunium = neptunium, plutonium = plutonium, americium = americium, curium = curium, berkelium = berkelium, californium = californium,\
		 	einsteinium = einsteinium, fermium = fermium, mendelevium = mendelevium, nobelium = nobelium, lawrencium = lawrencium,\
		 	rutherfordium = rutherfordium, dubnium = dubnium, seaborgium = seaborgium, bohrium = bohrium, hassium = hassium,\
		 	meitnerium = meitnerium, darmstadtium = darmstadtium, roentgenium = roentgenium, copernicium = copernicium, nihonium = nihonium,\
		 	flerovium = flerovium, moscovium = moscovium, livermorium = livermorium, tennessium = tennessium, oganesson = oganesson, comment = comment)

def remove_operation_state(timestamp):
	return remove(timestamp, 'operation_state', dicted = True)

#/api/create/operationstate/fields=ok&where=timestamp:'2017-02-12 23:59:59',operation:'e85b8f435d6f4867af90133d4e8807a2',boat:'5acd0904ee18bbcfe8035ae1',status:'finishing',distancetotheship:100.12,zenith:2.02,azimuth:3.03,hassium:80,helium:20,comment:'all is perfect'
#/api/remove/operationstate/fields=ok&where=timestamp:'2017-02-12 23:59:59'


if __name__ == '__main__':
	#print(remove_position(datetime.datetime.strptime('2017-02-12 23:59:59', TIMESTAMP_PATTERN)).date)
	print(create_position(datetime.datetime.strptime('2017-02-12 23:59:59', TIMESTAMP_PATTERN), 13.0, 13.0, 13.0, 10.0, 0.2, 0.2).time)