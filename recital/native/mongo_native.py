from pymongo import MongoClient
import configparser
import sys, os, re

from bson.objectid import ObjectId

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MONGO_DB_URL = os.environ.get('MONGO_DB_URL') if os.environ.get('MONGO_DB_URL') else config['MONGO']['host']
MONGO_DB_PORT = int(os.environ.get('MONGO_DB_PORT') if os.environ.get('MONGO_DB_PORT') else config['MONGO']['port'])
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') if os.environ.get('MONGO_DB_NAME') else config['MONGO']['db_name']

db = MongoClient(MONGO_DB_URL, MONGO_DB_PORT)[MONGO_DB_NAME]

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/logbook/adapters')

import neo4j_adapter

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations')

import neo4j_mediator

##

def get_item_ids_with_foreign_id(collection_name, property_name, id):
	object_id = ObjectId(id)
	return [str(item['_id']) for item in db[collection_name].find({property_name : object_id}, {'_id' : 1})]

##


def get_all_items_ids(collection_name):
	return [str(item['_id']) for item in db[collection_name].find({}, {'_id' : 1})]

def get_properties_with_department(department_id):
	department_object_id = ObjectId(department_id)
	return [item for item in db['property_test'].find({'department' : department_object_id})]

def get_properties_with_type(type_id):
	type_object_id = ObjectId(type_id)
	return [item for item in db['property_test'].find({'type' : type_object_id})]

def get_people_ids_with_spec(specialization_id):
	specialization_object_id = ObjectId(specialization_id)
	return [str(item['_id']) for item in db['people_test'].find({'specialization' : specialization_object_id}, {'_id' : 1})]

def get_people_ids_with_dep(department_id):
	department_object_id = ObjectId(department_id)
	return [str(item['_id']) for item in db['people_test'].find({'department' : department_object_id}, {'_id' : 1})]

def get_system_ids_with_type(type_id):
	type_object_id = ObjectId(type_id)
	return [str(item['_id']) for item in db['people_test'].find({'department' : department_object_id}, {'_id' : 1})]

def get_sensors_by_location_id(location_id):
	location_object_id = ObjectId(location_id)
	return [item for item in db['source_test'].find({'location' : location_object_id})]

def get_sensors_ids_by_location_id(location_id):
	location_object_id = ObjectId(location_id)
	return [str(item['_id']) for item in db['source_test'].find({'location' : location_object_id}, {'_id' : 1})]

def get_systems_by_state_id(state_id):
	state_object_id = ObjectId(state_id)
	return [item for item in db['sys_test'].find({'state' : state_object_id})]

def get_systems_by_type_id(type_id):
	type_object_id = ObjectId(type_id)
	return [item for item in db['sys_test'].find({'type' : type_object_id})]

def get_systems_by_supervisor_id(supervisor_id):
	supervisor_object_id = ObjectId(supervisor_id)
	return [item for item in db['sys_test'].find({'supervisor' : supervisor_object_id})]

def get_all_items(collection_name):
	return [item for item in db[collection_name].find()]

def get_item_by_id(collection_name, id):
	return db[collection_name].find({'_id' : ObjectId(id)})[0]

def get_all_people_ids():
    return get_all_items_ids('people_test')

def get_all_departments_ids():
    return get_all_items_ids('department_test')

def get_all_specializations_ids():
    return get_all_items_ids('spec_test')

def get_all_property_types():
    return get_all_items('property_type_test')

def get_all_systems():
    return get_all_items('sys_test')

def get_property_type_by_id(id):
    return get_item_by_id('property_type_test', id)

def get_location_by_id(id):
    return get_item_by_id('location_test', id)

def get_boat_by_id(id):
    return get_item_by_id('boat_test', id)

def get_person_by_id(id):
    return get_item_by_id('people_test', id)

def get_sensor_by_id(id):
    return get_item_by_id('source_test', id)

def get_department_by_id(id):
    return get_item_by_id('department_test', id)

def get_specialization_by_id(id):
    return get_item_by_id('spec_test', id)

def get_system_state_by_id(id):
    return get_item_by_id('system_state_test', id)

def get_system_type_by_id(id):
    return get_item_by_id('system_types_test', id)

def get_system_by_id(id):
    return get_item_by_id('sys_test', id)

def get_property_by_id(id):
    return get_item_by_id('property_test', id)

def get_all_properties():
    return get_all_items('property_test')

def get_all_system_states():
    return get_all_items('system_state_test')

def get_all_system_types():
    return get_all_items('system_types_test')

def get_all_locations():
    return get_all_items('location_test')

def get_all_boats():
    return get_all_items('boat_test')

def get_all_sensors():
    return get_all_items('source_test')

## location manipulator

def create_location(name):
	id = db['location_test'].insert({'name' : name})
	return get_location_by_id(str(id))

def remove_location(id):
	deleted = get_location_by_id(str(id))
	id = db['location_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_location(id):
	deleted_sensors = get_sensors_ids_by_location_id(str(id))
	print(deleted_sensors)
	for sensor_id in deleted_sensors:
		remove_sensor(sensor_id)
	return remove_location(id)

## sensor manipulator

def create_sensor(name, location):
	print('omg')
	id = db['source_test'].insert({'name' : name, 'location' : ObjectId(location)})
	return get_sensor_by_id(str(id))

def remove_sensor(id):
	print(id)
	deleted = get_sensor_by_id(str(id))
	id = db['source_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

## department manipulator

def create_department(name, vk):
	id = db['department_test'].insert({'name' : name, 'vk' : vk})
	return get_department_by_id(str(id))

def remove_department(id):
	#print(id)
	deleted = get_department_by_id(str(id))
	id = db['department_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_department(id):
	deleted_people = get_people_ids_with_dep(str(id))
	print(deleted_people)

	for property_id in get_item_ids_with_foreign_id('property_test', 'department', str(id)):
		remove_property(property_id)
	
	for person_id in deleted_people:
		remove_person(person_id)
	return remove_department(id)

## person manipulator

def create_person(name, surname, patronymic, phone, department, specialization):
	id = db['people_test'].insert({'name' : name, 'surname' : surname, 'patronymic' : patronymic, 'phone' : phone, 'department' : ObjectId(department), 'specialization' : ObjectId(specialization)})
	return get_person_by_id(str(id))

def remove_person(id):
	#print(id)
	deleted = get_person_by_id(str(id))
	print(deleted)
	id = db['people_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_person(id):
	deleted_chiefed_shifts = [item['ident'] for item in neo4j_adapter.get_chiefed_shifts(id)]
	for shift_id in deleted_chiefed_shifts:
		neo4j_mediator.remove_shift(shift_id)

	deleted_headed_operations = [item['ident'] for item in neo4j_adapter.get_headed_operations(id)]
	for operation_id in deleted_headed_operations:
		neo4j_mediator.remove_operation(operation_id)

	return remove_person(id)

## specialization manipulator

def create_specialization(name):
	id = db['spec_test'].insert({'name' : name})
	return get_specialization_by_id(str(id))

def remove_specialization(id):
	#print(id)
	deleted = get_specialization_by_id(str(id))
	id = db['spec_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_specialization(id):
	deleted_people = get_people_ids_with_spec(str(id))
	print(deleted_people)
	for person_id in deleted_people:
		remove_person(person_id)
	return remove_specialization(id)

## boat manipulator

def create_boat(name, capacity):
	print('omg')
	id = db['boat_test'].insert({'name' : name, 'capacity' : capacity})
	return get_boat_by_id(str(id))

def remove_boat(id):
	print(id)
	deleted = get_boat_by_id(str(id))
	id = db['boat_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

## system type manipulator

def create_system_type(name, description):
	print('omg')
	id = db['system_types_test'].insert({'name' : name, 'description' : description})
	return get_system_type_by_id(str(id))

def remove_system_type(id):
	print(id)
	deleted = get_system_type_by_id(str(id))
	id = db['system_types_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_system_type(id):
	deleted_systems = get_item_ids_with_foreign_id('sys_test', 'type', str(id))
	for system_id in deleted_systems:
		remove_system(system_id)
	return remove_system_type(id)

## system state manipulator

def create_system_state(name, description):
	print('omg')
	id = db['system_state_test'].insert({'name' : name, 'description' : description})
	return get_system_state_by_id(str(id))

def remove_system_state(id):
	print(id)
	deleted = get_system_state_by_id(str(id))
	id = db['system_state_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_system_state(id):
	deleted_systems = get_item_ids_with_foreign_id('sys_test', 'state', str(id))
	for system_id in deleted_systems:
		remove_system(system_id)
	return remove_system_state(id)

## property type manipulator

def create_property_type(name, description):
	print('omg')
	id = db['property_type_test'].insert({'name' : name, 'description' : description})
	return get_property_type_by_id(str(id))

def remove_property_type(id):
	print(id)
	deleted = get_property_type_by_id(str(id))
	id = db['property_type_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_property_type(id):
	for property_id in get_item_ids_with_foreign_id('property_test', 'type', str(id)):
		remove_property(property_id)
	return remove_property_type(id)

## system manipulator

def create_system(name, serial_number, launched, checked, state, supervisor, type):
	id = db['sys_test'].insert({'name': name, 'serial_number': serial_number, 'launched': launched,\
		'checked': checked, 'state': ObjectId(state), 'supervisor': ObjectId(supervisor), 'type': ObjectId(type)})
	return get_system_by_id(str(id))

def remove_system(id):
	deleted = get_system_by_id(str(id))
	id = db['sys_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

## property manipulator

def create_property(name, type, admission, comissioning, department):
	id = db['property_test'].insert({'name': name, 'type': ObjectId(type), 'admission': admission,\
		'comissioning': comissioning, 'department': ObjectId(department)})
	return get_property_by_id(str(id))

def remove_property(id):
	deleted = get_property_by_id(str(id))
	id = db['property_test'].delete_one({'_id' : ObjectId(id)})
	return deleted

###

if __name__ == '__main__':
	print(create_location('test loc'))
	#print(get_all_properties())
	#print(get_people_ids_with_spec('5ac52207cc314386b6f43441'))
	#print(get_all_property_types())
	#print(get_all_ids('system_test'))