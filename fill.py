import os
from json_corrector import convert

from subprocess import call

def main():
	print(call(['mongoimport', '--db', 'test', '--collection', 'boats', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/boats.json', 'boats')]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'departments', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/department.json', 'department')]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'locations', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/locations.json', 'locations')]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'peoples', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/people.json', 'people', ['specialization', 'department'])]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'properties', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/properties.json', 'properties', ['type', 'department'])]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'propertyTypes', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/propertyTypes.json', 'propertyTypes')]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'sensors', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/sensors.json', 'sensors', ['location'])]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'specializations', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/specializations.json', 'specializations')]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'states', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/states.json', 'states')]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'systemss', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/systems.json', 'systems', ['type', 'state', 'personInCharge'])]))
	print(call(['mongoimport', '--db', 'test', '--collection', 'systemTypes', '--file', 
		convert(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/systemTypes.json', 'systemTypes')]))


if __name__ == '__main__':
	main()

