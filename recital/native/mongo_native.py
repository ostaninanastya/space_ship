from pymongo import MongoClient
import configparser
import sys, os, re

from bson.objectid import ObjectId

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MONGO_DB_URL = os.environ.get('MONGO_DB_URL') if os.environ.get('MONGO_DB_URL') else config['MONGO']['host']
MONGO_DB_PORT = int(os.environ.get('MONGO_DB_PORT') if os.environ.get('MONGO_DB_PORT') else config['MONGO']['port'])
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') if os.environ.get('MONGO_DB_NAME') else config['MONGO']['db_name']

BOATS_COLLECTION_NAME = os.environ.get('BOATS_COLLECTION_NAME') or config['MONGO']['boats_collection_name']
DEPARTMENTS_COLLECTION_NAME = os.environ.get('DEPARTMENTS_COLLECTION_NAME') or config['MONGO']['departments_collection_name']
LOCATIONS_COLLECTION_NAME = os.environ.get('LOCATIONS_COLLECTION_NAME') or config['MONGO']['locations_collection_name']
PEOPLE_COLLECTION_NAME = os.environ.get('PEOPLE_COLLECTION_NAME') or config['MONGO']['people_collection_name']
PROPERTIES_COLLECTION_NAME = os.environ.get('PROPERTIES_COLLECTION_NAME') or config['MONGO']['properties_collection_name']
PROPERTY_TYPES_COLLECTION_NAME = os.environ.get('PROPERTY_TYPES_COLLECTION_NAME') or config['MONGO']['property_types_collection_name']
SENSORS_COLLECTION_NAME = os.environ.get('SENSORS_COLLECTION_NAME') or config['MONGO']['sensors_collection_name']
SPECIALIZATIONS_COLLECTION_NAME = os.environ.get('SPECIALIZATIONS_COLLECTION_NAME') or config['MONGO']['specializations_collection_name']
SYSTEM_STATES_COLLECTION_NAME = os.environ.get('SYSTEM_STATES_COLLECTION_NAME') or config['MONGO']['system_states_collection_name']
SYSTEM_TYPES_COLLECTION_NAME = os.environ.get('SYSTEM_TYPES_COLLECTION_NAME') or config['MONGO']['system_types_collection_name']
SYSTEMS_COLLECTION_NAME = os.environ.get('SYSTEMS_COLLECTION_NAME') or config['MONGO']['systems_collection_name']

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
	return [item for item in db[PROPERTIES_COLLECTION_NAME].find({'department' : department_object_id})]

def get_properties_with_type(type_id):
	type_object_id = ObjectId(type_id)
	return [item for item in db[PROPERTIES_COLLECTION_NAME].find({'type' : type_object_id})]

def get_people_ids_with_spec(specialization_id):
	specialization_object_id = ObjectId(specialization_id)
	return [str(item['_id']) for item in db[PEOPLE_COLLECTION_NAME].find({'specialization' : specialization_object_id}, {'_id' : 1})]

def get_people_ids_with_dep(department_id):
	department_object_id = ObjectId(department_id)
	return [str(item['_id']) for item in db[PEOPLE_COLLECTION_NAME].find({'department' : department_object_id}, {'_id' : 1})]

def get_system_ids_with_type(type_id):
	type_object_id = ObjectId(type_id)
	return [str(item['_id']) for item in db[PEOPLE_COLLECTION_NAME].find({'department' : department_object_id}, {'_id' : 1})]

def get_sensors_by_location_id(location_id):
	location_object_id = ObjectId(location_id)
	return [item for item in db[SENSORS_COLLECTION_NAME].find({'location' : location_object_id})]

def get_sensors_ids_by_location_id(location_id):
	location_object_id = ObjectId(location_id)
	return [str(item['_id']) for item in db[SENSORS_COLLECTION_NAME].find({'location' : location_object_id}, {'_id' : 1})]

def get_systems_by_state_id(state_id):
	state_object_id = ObjectId(state_id)
	return [item for item in db[SYSTEMS_COLLECTION_NAME].find({'state' : state_object_id})]

def get_systems_by_type_id(type_id):
	type_object_id = ObjectId(type_id)
	return [item for item in db[SYSTEMS_COLLECTION_NAME].find({'type' : type_object_id})]

def get_systems_by_supervisor_id(supervisor_id):
	supervisor_object_id = ObjectId(supervisor_id)
	return [item for item in db[SYSTEMS_COLLECTION_NAME].find({'supervisor' : supervisor_object_id})]

def get_all_items(collection_name):
	return [item for item in db[collection_name].find()]

def get_item_by_id(collection_name, id):
	return db[collection_name].find({'_id' : ObjectId(id)})[0]

def get_all_people_ids():
    return get_all_items_ids(PEOPLE_COLLECTION_NAME)

def get_all_departments_ids():
    return get_all_items_ids(DEPARTMENTS_COLLECTION_NAME)

def get_all_specializations_ids():
    return get_all_items_ids(SPECIALIZATIONS_COLLECTION_NAME)

def get_all_property_types():
    return get_all_items(PROPERTY_TYPES_COLLECTION_NAME)

def get_all_systems():
    return get_all_items(SYSTEMS_COLLECTION_NAME)

def get_property_type_by_id(id):
    return get_item_by_id(PROPERTY_TYPES_COLLECTION_NAME, id)

def get_location_by_id(id):
    return get_item_by_id(LOCATIONS_COLLECTION_NAME, id)

def get_boat_by_id(id):
    return get_item_by_id(BOATS_COLLECTION_NAME, id)

def get_person_by_id(id):
    return get_item_by_id(PEOPLE_COLLECTION_NAME, id)

def get_sensor_by_id(id):
    return get_item_by_id(SENSORS_COLLECTION_NAME, id)

def get_department_by_id(id):
    return get_item_by_id(DEPARTMENTS_COLLECTION_NAME, id)

def get_specialization_by_id(id):
    return get_item_by_id(SPECIALIZATIONS_COLLECTION_NAME, id)

def get_system_state_by_id(id):
    return get_item_by_id(SYSTEM_STATES_COLLECTION_NAME, id)

def get_system_type_by_id(id):
    return get_item_by_id(SYSTEM_TYPES_COLLECTION_NAME, id)

def get_system_by_id(id):
    return get_item_by_id(SYSTEMS_COLLECTION_NAME, id)

def get_property_by_id(id):
    return get_item_by_id(PROPERTIES_COLLECTION_NAME, id)

def get_all_properties():
    return get_all_items(PROPERTIES_COLLECTION_NAME)

def get_all_system_states():
    return get_all_items(SYSTEM_STATES_COLLECTION_NAME)

def get_all_system_types():
    return get_all_items(SYSTEM_TYPES_COLLECTION_NAME)

def get_all_locations():
    return get_all_items(LOCATIONS_COLLECTION_NAME)

def get_all_boats():
    return get_all_items(BOATS_COLLECTION_NAME)

def get_all_sensors():
    return get_all_items(SENSORS_COLLECTION_NAME)

## location manipulator

def create_location(name):
	id = db[LOCATIONS_COLLECTION_NAME].insert({'name' : name})
	return get_location_by_id(str(id))

def remove_location(id):
	deleted = get_location_by_id(str(id))
	id = db[LOCATIONS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_location(id):
	deleted_sensors = get_sensors_ids_by_location_id(str(id))
	#print(deleted_sensors)
	for sensor_id in deleted_sensors:
		remove_sensor(sensor_id)
	return remove_location(id)

## sensor manipulator

def create_sensor(name, location):
	#print('omg')
	id = db[SENSORS_COLLECTION_NAME].insert({'name' : name, 'location' : ObjectId(location)})
	return get_sensor_by_id(str(id))

def remove_sensor(id):
	#print(id)
	deleted = get_sensor_by_id(str(id))
	id = db[SENSORS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

## department manipulator

def create_department(name, vk):
	id = db[DEPARTMENTS_COLLECTION_NAME].insert({'name' : name, 'vk' : vk})
	return get_department_by_id(str(id))

def remove_department(id):
	#print(id)
	deleted = get_department_by_id(str(id))
	id = db[DEPARTMENTS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_department(id):
	deleted_people = get_people_ids_with_dep(str(id))
	#print(deleted_people)

	for property_id in get_item_ids_with_foreign_id(PROPERTIES_COLLECTION_NAME, 'department', str(id)):
		remove_property(property_id)
	
	for person_id in deleted_people:
		remove_person(person_id)
	return remove_department(id)

## person manipulator

def create_person(name, surname, patronymic, phone, department, specialization):
	id = db[PEOPLE_COLLECTION_NAME].insert({'name' : name, 'surname' : surname, 'patronymic' : patronymic, 'phone' : phone, 'department' : ObjectId(department), 'specialization' : ObjectId(specialization)})
	return get_person_by_id(str(id))

def remove_person(id):
	#print(id)
	deleted = get_person_by_id(str(id))
	#print(deleted)
	id = db[PEOPLE_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
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
	id = db[SPECIALIZATIONS_COLLECTION_NAME].insert({'name' : name})
	return get_specialization_by_id(str(id))

def remove_specialization(id):
	#print(id)
	deleted = get_specialization_by_id(str(id))
	id = db[SPECIALIZATIONS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_specialization(id):
	deleted_people = get_people_ids_with_spec(str(id))
	#print(deleted_people)
	for person_id in deleted_people:
		remove_person(person_id)
	return remove_specialization(id)

## boat manipulator

def create_boat(name, capacity):
	#print('omg')
	id = db[BOATS_COLLECTION_NAME].insert({'name' : name, 'capacity' : capacity})
	return get_boat_by_id(str(id))

def remove_boat(id):
	#print(id)
	deleted = get_boat_by_id(str(id))
	id = db[BOATS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

## system type manipulator

def create_system_type(name, description):
	#print('omg')
	id = db[SYSTEM_TYPES_COLLECTION_NAME].insert({'name' : name, 'description' : description})
	return get_system_type_by_id(str(id))

def remove_system_type(id):
	#print(id)
	deleted = get_system_type_by_id(str(id))
	id = db[SYSTEM_TYPES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_system_type(id):
	deleted_systems = get_item_ids_with_foreign_id(SYSTEMS_COLLECTION_NAME, 'type', str(id))
	for system_id in deleted_systems:
		remove_system(system_id)
	return remove_system_type(id)

## system state manipulator

def create_system_state(name, description):
	#print('omg')
	id = db[SYSTEM_STATES_COLLECTION_NAME].insert({'name' : name, 'description' : description})
	return get_system_state_by_id(str(id))

def remove_system_state(id):
	#print(id)
	deleted = get_system_state_by_id(str(id))
	id = db[SYSTEM_STATES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_system_state(id):
	deleted_systems = get_item_ids_with_foreign_id(SYSTEMS_COLLECTION_NAME, 'state', str(id))
	for system_id in deleted_systems:
		remove_system(system_id)
	return remove_system_state(id)

## property type manipulator

def create_property_type(name, description):
	#print('omg')
	id = db[PROPERTY_TYPES_COLLECTION_NAME].insert({'name' : name, 'description' : description})
	return get_property_type_by_id(str(id))

def remove_property_type(id):
	#print(id)
	deleted = get_property_type_by_id(str(id))
	id = db[PROPERTY_TYPES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

def eradicate_property_type(id):
	for property_id in get_item_ids_with_foreign_id(PROPERTIES_COLLECTION_NAME, 'type', str(id)):
		remove_property(property_id)
	return remove_property_type(id)

## system manipulator

def create_system(name, serial_number, launched, checked, state, supervisor, type):
	id = db[SYSTEMS_COLLECTION_NAME].insert({'name': name, 'serial_number': serial_number, 'launched': launched,\
		'checked': checked, 'state': ObjectId(state), 'supervisor': ObjectId(supervisor), 'type': ObjectId(type)})
	return get_system_by_id(str(id))

def remove_system(id):
	deleted = get_system_by_id(str(id))
	id = db[SYSTEMS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

## property manipulator

def create_property(name, type, admission, comissioning, department):
	id = db[PROPERTIES_COLLECTION_NAME].insert({'name': name, 'type': ObjectId(type), 'admission': admission,\
		'comissioning': comissioning, 'department': ObjectId(department)})
	return get_property_by_id(str(id))

def remove_property(id):
	deleted = get_property_by_id(str(id))
	id = db[PROPERTIES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	return deleted

###

def parse_params_for_update(params):

	where = {}
	update = {}

	for key in params:
		if params[key]:
			if 'set_' in key:
				update[key.replace('set_','')] = params[key]
				continue
			else:
				where[key] = params[key]

	return where, update

def update(params, collection):
	where, update = parse_params_for_update(params)
	db[collection].update_many(where,{'$set': update})
	return [item for item in db[collection].find(update)]

def update_sensor(**kwargs):
	return update(kwargs, SENSORS_COLLECTION_NAME)

def update_people(**kwargs):
	return update(kwargs, PEOPLE_COLLECTION_NAME)

def update_departments(**kwargs):
	return update(kwargs, DEPARTMENTS_COLLECTION_NAME)

def update_locations(**kwargs):
	return update(kwargs, LOCATIONS_COLLECTION_NAME)

def update_property_types(**kwargs):
	return update(kwargs, PROPERTY_TYPES_COLLECTION_NAME)

def update_specializations(**kwargs):
	return update(kwargs, SPECIALIZATIONS_COLLECTION_NAME)

def update_boats(**kwargs):
	return update(kwargs, BOATS_COLLECTION_NAME)

def update_system_types(**kwargs):
	return update(kwargs, SYSTEM_TYPES_COLLECTION_NAME)

def update_system_states(**kwargs):
	return update(kwargs, SYSTEM_STATES_COLLECTION_NAME)

def update_systems(**kwargs):
	return update(kwargs, SYSTEMS_COLLECTION_NAME)

def update_properties(**kwargs):
	return update(kwargs, PROPERTIES_COLLECTION_NAME)

###

def parse_params_for_select(params):

	where = {}

	for key in params:
		if params[key]:
			if isinstance(params[key], str):
				where[key] = {'$regex' : params[key], '$options' : 'i'}
			else:
				where[key] = params[key]

	return where

def select(params, collection):
	#print(parse_params_for_select(params))
	return [item for item in db[collection].find(parse_params_for_select(params))]

def select_sensors(**kwargs):
	return select(kwargs, SENSORS_COLLECTION_NAME)

def select_people(**kwargs):
	return select(kwargs, PEOPLE_COLLECTION_NAME)

def select_departments(**kwargs):
	return select(kwargs, DEPARTMENTS_COLLECTION_NAME)

def select_locations(**kwargs):
	return select(kwargs, LOCATIONS_COLLECTION_NAME)

def select_property_types(**kwargs):
	return select(kwargs, PROPERTY_TYPES_COLLECTION_NAME)

def select_specializations(**kwargs):
	return select(kwargs, SPECIALIZATIONS_COLLECTION_NAME)

def select_boats(**kwargs):
	return select(kwargs, BOATS_COLLECTION_NAME)

def select_system_types(**kwargs):
	return select(kwargs, SYSTEM_TYPES_COLLECTION_NAME)

def select_system_states(**kwargs):
	return select(kwargs, SYSTEM_STATES_COLLECTION_NAME)

def select_systems(**kwargs):
	return select(kwargs, SYSTEMS_COLLECTION_NAME)

def select_properties(**kwargs):
	return select(kwargs, PROPERTIES_COLLECTION_NAME)

if __name__ == '__main__':
	print(update_people(name = 'dima', set_name = 'dimas'))
	#print(select_sensor(name = 'o'))
	#print(create_location('test loc'))
	#print(get_all_properties())
	#print(get_people_ids_with_spec('5ac52207cc314386b6f43441'))
	#print(get_all_property_types())
	#print(get_all_ids('system_test'))