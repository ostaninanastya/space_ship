

# import


import configparser
import sys, os, re, math
import datetime
from bson.objectid import ObjectId
from bson.binary import Binary
import time

import pymongo
from pymongo import MongoClient, UpdateOne

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/logbook/adapters')

import neo4j_adapter

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations')

import neo4j_mediator

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/transporters')

import frontal_transporter


# set global constants


config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MONGO_DB_URL = os.environ.get('MONGO_DB_URL') if os.environ.get('MONGO_DB_URL') else config['MONGO']['host']
MONGO_DB_PORT = int(os.environ.get('MONGO_DB_PORT') if os.environ.get('MONGO_DB_PORT') else config['MONGO']['port'])
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') if os.environ.get('MONGO_DB_NAME') else config['MONGO']['db_name']

# recital
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
# relations
SHIFTS_COLLECTION_NAME = os.environ.get('SHIFTS_COLLECTION_NAME') or config['MONGO']['shifts_collection_name']
OPERATIONS_COLLECTION_NAME = os.environ.get('OPERATIONS_COLLECTION_NAME') or config['MONGO']['operations_collection_name']
REQUIREMENTS_COLLECTION_NAME = os.environ.get('REQUIREMENTS_COLLECTION_NAME') or config['MONGO']['requirements_collection_name']
# logbook
SYSTEM_TESTS_COLLECTION_NAME = os.environ.get('SYSTEM_TESTS_COLLECTION_NAME') or config['MONGO']['system_tests_collection_name']
CONTROL_ACTIONS_COLLECTION_NAME = os.environ.get('CONTROL_ACTIONS_COLLECTION_NAME') or config['MONGO']['control_actions_collection_name']
POSITIONS_COLLECTION_NAME = os.environ.get('POSITIONS_COLLECTION_NAME') or config['MONGO']['positions_collection_name']
SENSOR_DATA_COLLECTION_NAME = os.environ.get('SENSOR_DATA_COLLECTION_NAME') or config['MONGO']['sensor_data_collection_name']
SHIFT_STATES_COLLECTION_NAME = os.environ.get('SHIFT_STATES_COLLECTION_NAME') or config['MONGO']['shift_states_collection_name']
OPERATION_STATES_COLLECTION_NAME = os.environ.get('OPERATION_STATES_COLLECTION_NAME') or config['MONGO']['operation_states_collection_name']

db = MongoClient(MONGO_DB_URL, MONGO_DB_PORT)[MONGO_DB_NAME]

ID_DELIMITER = ','
REQ_COMPONENT_DELIMITER = ':'

#------------------------------------------------------------------------------------------------
# general methods
#------------------------------------------------------------------------------------------------

def parse_objids_list(source):

	parsed = []

	for id in source.split(ID_DELIMITER):
		parsed.append(ObjectId(id))

	return parsed

# get

def get_items_with_foreign_id(collection_name, property_name, id):
	object_id = ObjectId(id)
	return [item for item in db[collection_name].find({property_name : object_id})]

def get_item_ids_with_foreign_id(collection_name, property_name, id):
	object_id = ObjectId(id)
	return [str(item['_id']) for item in db[collection_name].find({property_name: object_id}, {'_id' : 1})]

def get_all_items(collection_name):
	return [item for item in db[collection_name].find()]

def get_all_items_ids(collection_name):
	return [str(item['_id']) for item in db[collection_name].find({}, {'_id' : 1})]

def get_item_by_id(collection_name, id):
	return db[collection_name].find({'_id' : ObjectId(str(id).zfill(24))})[0]

# update

def parse_params_for_update(params, ids_fields):

	where = {}
	update = {}
	ids = {}
	select_where = {}

	for key in params:
		if params[key] and not math.isnan(params[key]):
			if 'set_' in key:
				update[key.replace('set_','')] = params[key]
				continue
			else:
				where[key] = params[key]
				if key in ids_fields:
					ids[ids_fields[key]] = params[key]
				else:
					select_where[key] = params[key] 

	select_where['ids'] = ids

	return where, update, select_where

def adjust_and_update(params, collection, lists_fields, id_fields):

	for field in lists_fields:
		if field in kwargs:
			params[field] = parse_objids_list(params[field]) if params[field] else None

	for field in id_fields:
		if field in kwargs:
			params[field] = ObjectId(params[field]) if params[field] else None

	return update(params, collection)

def update(params, collection):

	ids_fields = {'_id': '_id'}

	where, update, select_where = parse_params_for_update(params, ids_fields)

	#print(select_where)

	select(select_where, collection)

	db[collection].update_many(where,{'$set': update})
	return [item for item in db[collection].find(update)]

def remove(id, get_item, collection):
	
	select({'ids': {'_id': id}}, collection)

	deleted = get_item(str(id))

	id = deleted['_id']

	frontal_transporter.remove(collection, {'id': id})

	return deleted

#http://localhost:1881/api/remove/boat/fields=boat(name,id)&where=id:'5aedb8f1d678f40f92a279be'

# select

def parse_params_for_select(params):

	where = {}

	for key in params:
		if params[key] and not math.isnan(params[key]):
			if isinstance(params[key], str):
				where[key] = {'$regex' : params[key], '$options' : 'i'}
			else:
				where[key] = params[key]

	return where

def match_ids(item, regexps):
	for key in regexps:
		if not regexps[key].match(str(item[key])):
			return False
	return True

def filter_by_ids(items, ids):
	regexps = {}

	for key in ids:
		regexps[key] = re.compile(str(ids[key]) + '.*')

	return [item for item in items if match_ids(item, regexps)]

def select(params, collection):
	#print(parse_params_for_select(params))

	#print(params)

	ids = params.pop('ids', None)



	try:
		frontal_transporter.extract(params, collection)
	except pymongo.errors.DuplicateKeyError:
		pass
	
	parsed_params = parse_params_for_select(params)

	current_timestamp = datetime.datetime.now()
	items = [item for item in db[collection].find(parsed_params)]
	
	try:
		result = db[collection].bulk_write([UpdateOne({'_id' : record['_id']},
			{ 
				'$set':  { '__accessed__': current_timestamp}, 
				'$push': { '__gaps__': (current_timestamp - record['__accessed__']).total_seconds() }
			}) 
		for record in items])
	except KeyError:
		result = db[collection].bulk_write([UpdateOne({'_id' : record['_id']}, {'$set':  { '__accessed__': current_timestamp, '__gaps__': [0]}}) for record in items])
	
	print([item for item in db[collection].find(parsed_params)])

	#db[collection].update_many(parse_params_for_select(params), {'__accessed__': current_timestamp, '$push': { '__gaps__': int((current_timestamp - ).strftime("%s"))}})
	return filter_by_ids(items, ids)


	
	'''
	print(dir(db))

	bulk = db.coll.initialize_ordered_bulk_op()
	counter = 0

	for record in coll.find(parse_params_for_select(params), snapshot=True):
	    bulk.find({ '_id': record['_id'] }).update({ '$set': { '__accessed__': current_timestamp, '$push': { '__gaps__': int((current_timestamp - record['__accessed__']).strftime("%s")) } }})
	    counter += 1

	    if counter % 1000 == 0:
	        bulk.execute()
	        bulk = db.coll.initialize_ordered_bulk_op()

	if counter % 1000 != 0:
	    bulk.execute()

	return [item for item in db[collection].find(parse_params_for_select(params))]
	'''

#------------------------------------------------------------------------------------------------
# particular methods
#------------------------------------------------------------------------------------------------

# - boats ---------------------------------------------------------------------------------------

def get_all_boats():
    return get_all_items(BOATS_COLLECTION_NAME)

# -- by id

def get_boat_by_id(id):
    return get_item_by_id(BOATS_COLLECTION_NAME, id)

# -- manipulators

def create_boat(name, capacity):
	id = db[BOATS_COLLECTION_NAME].insert({'name': name, 'capacity': capacity, 
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_boat_by_id(str(id))

def remove_boat(id):
	return remove(id, get_boat_by_id, BOATS_COLLECTION_NAME)
	#deleted = get_boat_by_id(str(id))
	#id = db[BOATS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def update_boats(**kwargs):
	return update(kwargs, BOATS_COLLECTION_NAME)

def select_boats(**kwargs):
	return select(kwargs, BOATS_COLLECTION_NAME)

# - departments --------------------------------------------------------------------------------

def get_all_departments_ids():
    return get_all_items_ids(DEPARTMENTS_COLLECTION_NAME)

# -- by id

def get_department_by_id(id):
    return get_item_by_id(DEPARTMENTS_COLLECTION_NAME, id)

# -- manipulators

def create_department(name, vk, director):
	id = db[DEPARTMENTS_COLLECTION_NAME].insert({'name' : name, 'vk' : vk, 'director': ObjectId(director),
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_department_by_id(str(id))

def remove_department(id):
	return remove(id, get_department_by_id, DEPARTMENTS_COLLECTION_NAME)
	#deleted = get_department_by_id(str(id))
	#id = db[DEPARTMENTS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def eradicate_department(id):
	deleted_people = get_people_ids_with_dep(str(id))

	for property_id in get_item_ids_with_foreign_id(PROPERTIES_COLLECTION_NAME, 'department', str(id)):
		remove_property(property_id)
	
	for person_id in deleted_people:
		remove_person(person_id)

	return remove_department(id)

def update_departments(**kwargs):
	return update(kwargs, DEPARTMENTS_COLLECTION_NAME)

def select_departments(**kwargs):
	return select(kwargs, DEPARTMENTS_COLLECTION_NAME)

# - locations -----------------------------------------------------------------------------------

def get_all_locations():
    return get_all_items(LOCATIONS_COLLECTION_NAME)

# -- by id

def get_location_by_id(id):
    return get_item_by_id(LOCATIONS_COLLECTION_NAME, id)

# -- manipulators

def create_location(name):
	id = db[LOCATIONS_COLLECTION_NAME].insert({'name' : name,
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_location_by_id(str(id))

def remove_location(id):
	return remove(id, get_specialization_by_id, SPECIALIZATIONS_COLLECTION_NAME)
	#deleted = get_location_by_id(str(id))
	#id = db[LOCATIONS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def eradicate_location(id):
	deleted_sensors = get_sensors_ids_by_location_id(str(id))
	for sensor_id in deleted_sensors:
		remove_sensor(sensor_id)
	return remove_location(id)

def select_locations(**kwargs):
	return select(kwargs, LOCATIONS_COLLECTION_NAME)

def update_locations(**kwargs):
	return update(kwargs, LOCATIONS_COLLECTION_NAME)

# - people -----------------------------------------------------------------------------------

def get_all_people_ids():
    return get_all_items_ids(PEOPLE_COLLECTION_NAME)

# -- by id

def get_person_by_id(id):
    return get_item_by_id(PEOPLE_COLLECTION_NAME, id)

# -- by department

def get_people_with_department(department_id):
	return get_items_with_foreign_id(PEOPLE_COLLECTION_NAME, 'department', department_id)

def get_people_ids_with_dep(department_id):
	return get_item_ids_with_foreign_id(PEOPLE_COLLECTION_NAME, 'department', department_id)

def select_people(**kwargs):
	return select(kwargs, PEOPLE_COLLECTION_NAME)

# -- manipulators

def create_person(name, surname, patronymic, phone, department, specialization):
	id = db[PEOPLE_COLLECTION_NAME].insert({'name' : name, 'surname' : surname, 'patronymic' : patronymic, 
		'phone' : phone, 'department' : ObjectId(department), 'specialization' : ObjectId(specialization),
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_person_by_id(str(id))

def remove_person(id):
	return remove(id, get_person_by_id, PEOPLE_COLLECTION_NAME)
	#deleted = get_person_by_id(str(id))
	#id = db[PEOPLE_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def eradicate_person(id):

	deleted_chiefed_shifts = [item['ident'] for item in neo4j_adapter.get_chiefed_shifts(id)]

	for shift_id in deleted_chiefed_shifts:
		neo4j_mediator.remove_shift(shift_id)

	deleted_headed_operations = [item['ident'] for item in neo4j_adapter.get_headed_operations(id)]
	
	for operation_id in deleted_headed_operations:
		neo4j_mediator.remove_operation(operation_id)

	return remove_person(id)

def update_people(**kwargs):
	return update(kwargs, PEOPLE_COLLECTION_NAME)

# - properties ------------------------------------------------------------------------------

def get_all_properties():
    return get_all_items(PROPERTIES_COLLECTION_NAME)

# -- by id

def get_property_by_id(id):
    return get_item_by_id(PROPERTIES_COLLECTION_NAME, id)

# -- by department

def get_properties_with_department(department_id):
	return get_items_with_foreign_id(PROPERTIES_COLLECTION_NAME, 'department', department_id)

# -- by type

def get_properties_with_type(type_id):
	return get_items_with_foreign_id(PROPERTIES_COLLECTION_NAME, 'type', type_id)

# -- by specialization

def get_people_with_specialization(specialization_id):
	return get_items_with_foreign_id(PEOPLE_COLLECTION_NAME, 'specialization', specialization_id)

def get_people_ids_with_spec(specialization_id):
	return get_item_ids_with_foreign_id(PEOPLE_COLLECTION_NAME, 'specialization', specialization_id)

# -- manipulators

def create_property(name, type, admission, comissioning, department):
	id = db[PROPERTIES_COLLECTION_NAME].insert({'name': name, 'type': ObjectId(type), 'admission': admission,\
		'comissioning': comissioning, 'department': ObjectId(department),
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_property_by_id(str(id))

def remove_property(id):
	return remove(id, get_property_by_id, PROPERTIES_COLLECTION_NAME)
	#deleted = get_property_by_id(str(id))
	#id = db[PROPERTIES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def update_properties(**kwargs):
	return update(kwargs, PROPERTIES_COLLECTION_NAME)

def select_properties(**kwargs):
	return select(kwargs, PROPERTIES_COLLECTION_NAME)

# - property types -----------------------------------------------------------------------------

def get_all_property_types():
    return get_all_items(PROPERTY_TYPES_COLLECTION_NAME)

# -- by id

def get_property_type_by_id(id):
    return get_item_by_id(PROPERTY_TYPES_COLLECTION_NAME, id)

# -- manipulators

def create_property_type(name, description):
	id = db[PROPERTY_TYPES_COLLECTION_NAME].insert({'name' : name, 'description' : description,
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_property_type_by_id(str(id))

def remove_property_type(id):
	return remove(id, get_property_type_by_id, PROPERTY_TYPES_COLLECTION_NAME)
	#deleted = get_property_type_by_id(str(id))
	#id = db[PROPERTY_TYPES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def eradicate_property_type(id):
	for property_id in get_item_ids_with_foreign_id(PROPERTIES_COLLECTION_NAME, 'type', str(id)):
		remove_property(property_id)
	return remove_property_type(id)

def update_property_types(**kwargs):
	return update(kwargs, PROPERTY_TYPES_COLLECTION_NAME)

def select_property_types(**kwargs):
	return select(kwargs, PROPERTY_TYPES_COLLECTION_NAME)

# - sensors ------------------------------------------------------------------------------------

def get_all_sensors():
    return get_all_items(SENSORS_COLLECTION_NAME)

# -- by id

def get_sensor_by_id(id):
    return get_item_by_id(SENSORS_COLLECTION_NAME, id)

# -- by location

def get_sensors_by_location_id(location_id):
	return get_items_with_foreign_id(SENSORS_COLLECTION_NAME, 'location', location_id)

def get_sensors_ids_by_location_id(location_id):
	return get_item_ids_with_foreign_id(SENSORS_COLLECTION_NAME, 'location', location_id)

# -- manipulators

def create_sensor(name, location):
	id = db[SENSORS_COLLECTION_NAME].insert({'name': name, 'location': ObjectId(location),
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_sensor_by_id(str(id))

def remove_sensor(id):
	return remove(id, get_sensor_by_id, SENSORS_COLLECTION_NAME)
	#deleted = get_sensor_by_id(str(id))
	#id = db[SENSORS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def update_sensor(**kwargs):
	return update(kwargs, SENSORS_COLLECTION_NAME)

def select_sensors(**kwargs):
	return select(kwargs, SENSORS_COLLECTION_NAME)

# - specializations ----------------------------------------------------------------------------

def get_all_specializations_ids():
    return get_all_items_ids(SPECIALIZATIONS_COLLECTION_NAME)

# -- by id

def get_specialization_by_id(id):
    return get_item_by_id(SPECIALIZATIONS_COLLECTION_NAME, id)

# -- manipulators

def create_specialization(name):
	id = db[SPECIALIZATIONS_COLLECTION_NAME].insert({'name' : name,
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_specialization_by_id(str(id))

def remove_specialization(id):
	return remove(id, get_specialization_by_id, SPECIALIZATIONS_COLLECTION_NAME)
	#deleted = get_specialization_by_id(str(id))
	#id = db[SPECIALIZATIONS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def eradicate_specialization(id):
	deleted_people = get_people_ids_with_spec(str(id))
	for person_id in deleted_people:
		remove_person(person_id)
	return remove_specialization(id)

def update_specializations(**kwargs):
	return update(kwargs, SPECIALIZATIONS_COLLECTION_NAME)

def select_specializations(**kwargs):
	return select(kwargs, SPECIALIZATIONS_COLLECTION_NAME)

# - systems ------------------------------------------------------------------------------------

def get_all_systems():
    return get_all_items(SYSTEMS_COLLECTION_NAME)

# -- by id

def get_system_by_id(id):
    return get_item_by_id(SYSTEMS_COLLECTION_NAME, id)

# -- by type

def get_system_ids_with_type(type_id):
	return get_item_ids_with_foreign_id(SYSTEM_COLLECTION_NAME, 'type', type_id)

def get_systems_by_type_id(type_id):
	return get_items_with_foreign_id(SYSTEMS_COLLECTION_NAME, 'type', type_id)

# -- by state

def get_systems_by_state_id(state_id):
	return get_items_with_foreign_id(SYSTEMS_COLLECTION_NAME, 'state', state_id)

# -- by supervisor

def get_systems_by_supervisor_id(supervisor_id):
	return get_items_with_foreign_id(SYSTEMS_COLLECTION_NAME, 'supervisor', supervisor_id)

# -- manipulators

def create_system(name, serial_number, launched, checked, state, supervisor, type):
	id = db[SYSTEMS_COLLECTION_NAME].insert({'name': name, 'serial_number': serial_number, 'launched': launched,\
		'checked': checked, 'state': ObjectId(state), 'supervisor': ObjectId(supervisor), 'type': ObjectId(type),
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_system_by_id(str(id))

def remove_system(id):
	return remove(id, get_system_state_by_id, SYSTEM_STATES_COLLECTION_NAME)
	#deleted = get_system_by_id(str(id))
	#id = db[SYSTEMS_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def update_systems(**kwargs):
	return update(kwargs, SYSTEMS_COLLECTION_NAME)

def select_systems(**kwargs):
	return select(kwargs, SYSTEMS_COLLECTION_NAME)

# - system states -------------------------------------------------------------------------------

def get_all_system_states():
    return get_all_items(SYSTEM_STATES_COLLECTION_NAME)

# -- by id

def get_system_state_by_id(id):
    return get_item_by_id(SYSTEM_STATES_COLLECTION_NAME, id)

# -- manipulators

def create_system_state(name, description):
	id = db[SYSTEM_STATES_COLLECTION_NAME].insert({'name' : name, 'description' : description,
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_system_state_by_id(str(id))

def remove_system_state(id):
	return remove(id, get_system_state_by_id, SYSTEM_STATES_COLLECTION_NAME)
	#deleted = get_system_state_by_id(str(id))
	#id = db[SYSTEM_STATES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def eradicate_system_state(id):
	deleted_systems = get_item_ids_with_foreign_id(SYSTEMS_COLLECTION_NAME, 'state', str(id))
	for system_id in deleted_systems:
		remove_system(system_id)
	return remove_system_state(id)

def update_system_states(**kwargs):
	return update(kwargs, SYSTEM_STATES_COLLECTION_NAME)

def select_system_states(**kwargs):
	return select(kwargs, SYSTEM_STATES_COLLECTION_NAME)

# - system types -------------------------------------------------------------------------------

def get_all_system_types():
    return get_all_items(SYSTEM_TYPES_COLLECTION_NAME)

# -- by id

def get_system_type_by_id(id):
    return get_item_by_id(SYSTEM_TYPES_COLLECTION_NAME, id)

# -- manipulators

def create_system_type(name, description):
	id = db[SYSTEM_TYPES_COLLECTION_NAME].insert({'name' : name, 'description' : description,
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_system_type_by_id(str(id))

def remove_system_type(id):
	return remove(id, get_system_type_by_id, SYSTEM_TYPES_COLLECTION_NAME)
	#deleted = get_system_type_by_id(str(id))
	#id = db[SYSTEM_TYPES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def eradicate_system_type(id):
	deleted_systems = get_item_ids_with_foreign_id(SYSTEMS_COLLECTION_NAME, 'type', str(id))
	for system_id in deleted_systems:
		remove_system(system_id)
	return remove_system_type(id)

def update_system_types(**kwargs):
	return update(kwargs, SYSTEM_TYPES_COLLECTION_NAME)

def select_system_types(**kwargs):
	return select(kwargs, SYSTEM_TYPES_COLLECTION_NAME)

# - shifts -------------------------------------------------------------------------------------

def get_all_shifts():
    return get_all_items(SHIFTS_COLLECTION_NAME)

# -- by id

def get_shift_by_id(id):
    return get_item_by_id(SHIFTS_COLLECTION_NAME, id)

# -- manipulators

def create_shift(chief, department, start, end, workers, requirements):
	id = db[SHIFTS_COLLECTION_NAME].insert({'start' : start, 'end' : end, 'department': ObjectId(department),
		'chief': ObjectId(chief), 'workers': parse_objids_list(workers), 'requirements': parse_objids_list(requirements),
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_shift_by_id(str(id))

def remove_shift(id):
	return remove(id, get_shift_by_id, SHIFTS_COLLECTION_NAME)
	#deleted = get_system_type_by_id(str(id))
	#id = db[SYSTEM_TYPES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def update_shifts(**kwargs):
	lists_fields = ['set_workers', 'workers', 'set_requirements', 'requirements']
	id_fields = ['set_chief', 'chief', 'set_department', 'department']
	return adjust_and_update(kwargs, SHIFTS_COLLECTION_NAME, lists_fields, id_fields)

def select_shifts(**kwargs):
	return select(kwargs, SHIFTS_COLLECTION_NAME)

# - operations ---------------------------------------------------------------------------------

def get_all_operations():
    return get_all_items(OPERATIONS_COLLECTION_NAME)

# -- by id

def get_operation_by_id(id):
    return get_item_by_id(OPERATIONS_COLLECTION_NAME, id)

# -- manipulators

def create_operation(name, head, start, end, executors, requirements):
	id = db[OPERATIONS_COLLECTION_NAME].insert({'name': name, 'start' : start, 'end' : end,
		'head': ObjectId(head), 'executors': parse_objids_list(executors), 'requirements': parse_objids_list(requirements),
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_operation_by_id(str(id))

def remove_operation(id):
	return remove(id, get_operation_by_id, OPERATIONS_COLLECTION_NAME)
	#deleted = get_system_type_by_id(str(id))
	#id = db[SYSTEM_TYPES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted

def update_operations(**kwargs):
	lists_fields = ['set_executors', 'executors', 'set_requirements', 'requirements']
	id_fields = ['set_head', 'head']
	return adjust_and_update(kwargs, OPERATIONS_COLLECTION_NAME, lists_fields, id_fields)

def select_operations(**kwargs):
	return select(kwargs, OPERATIONS_COLLECTION_NAME)

# - requirements -------------------------------------------------------------------------------

def get_all_requirements():
    return get_all_items(REQUIREMENTS_COLLECTION_NAME)

# -- by id

def get_requirement_by_id(id):
    return get_item_by_id(REQUIREMENTS_COLLECTION_NAME, id)

# -- manipulators

def create_requirement(name, content):

	requirement_parts = []
	
	for requirement_str_part in content.split(ID_DELIMITER):
		specialization, quantity = requirement_str_part.split(REQ_COMPONENT_DELIMITER)
		requirement_parts.append({'specialization' : ObjectId(specialization), 'quantity' : int(quantity)})

	id = db[REQUIREMENTS_COLLECTION_NAME].insert({'name': name, 'content': requirement_parts,
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_requirement_by_id(str(id))

def remove_requirement(id):
	return remove(id, get_requirement_by_id, REQUIREMENTS_COLLECTION_NAME)
	#deleted = get_system_type_by_id(str(id))
	#id = db[SYSTEM_TYPES_COLLECTION_NAME].delete_one({'_id' : ObjectId(id)})
	#return deleted
'''
def update_requirements(**kwargs):
	lists_fields = ['set_', 'executors', 'set_requirements', 'requirements']
	id_fields = ['set_head', 'head']
	return adjust_and_update(kwargs, OPERATIONS_COLLECTION_NAME, lists_fields, id_fields)
'''
def select_requirements(**kwargs):
	return select(kwargs, REQUIREMENTS_COLLECTION_NAME)

# //////////////////////////////////////////////////////////////////////////////////////////////
# logbook //////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////

# - system_tests -------------------------------------------------------------------------------

def get_all_system_tests():
    return get_all_items(SYSTEM_TESTS_COLLECTION_NAME)

# -- by id

def get_system_test_by_id(id):
    return get_item_by_id(SYSTEM_TESTS_COLLECTION_NAME, id)

# -- manipulators

def create_system_test(timestamp, system, result):
	id = db[SYSTEM_TESTS_COLLECTION_NAME].insert({'timestamp': timestamp, 'system' : ObjectId(system), 'result' : result,
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_system_test_by_id(str(id))

def remove_system_test(id):
	return remove(id, get_system_test_by_id, SYSTEM_TESTS_COLLECTION_NAME)

def update_system_tests(**kwargs):
	id_fields = ['set_system', 'system']
	return adjust_and_update(kwargs, SYSTEM_TESTS_COLLECTION_NAME, None, id_fields)

def select_system_tests(**kwargs):
	return select(kwargs, SYSTEM_TESTS_COLLECTION_NAME)

# - control_actions ----------------------------------------------------------------------------

def get_all_control_actions():
    return get_all_items(CONTROL_ACTIONS_COLLECTION_NAME)

# -- by id

def get_control_action_by_id(id):
    return get_item_by_id(CONTROL_ACTIONS_COLLECTION_NAME, id)

# -- manipulators

def create_control_action(timestamp, mac, user, command, params, result):
	id = db[CONTROL_ACTIONS_COLLECTION_NAME].insert({'timestamp': timestamp, 'mac_address': bytes.fromhex(mac.hex()), 'user' : ObjectId(user),
		'command': command, 'params': params, 'result': result,
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_control_action_by_id(str(id))

def remove_control_action(id):
	return remove(id, get_control_action_by_id, CONTROL_ACTIONS_COLLECTION_NAME)

def update_control_actions(**kwargs):
	id_fields = ['set_user', 'user']
	return adjust_and_update(kwargs, CONTROL_ACTIONS_COLLECTION_NAME, None, id_fields)

def select_control_actions(**kwargs):
	return select(kwargs, CONTROL_ACTIONS_COLLECTION_NAME)

# - positions ----------------------------------------------------------------------------------

def get_all_positions():
    return get_all_items(POSITIONS_COLLECTION_NAME)

# -- by id

def get_position_by_id(id):
    return get_item_by_id(POSITIONS_COLLECTION_NAME, id)

# -- manipulators

def create_position(timestamp, x, y, z, speed, attack_angle, direction_angle):
	id = db[POSITIONS_COLLECTION_NAME].insert({'timestamp': timestamp, 'attack_angle': attack_angle, 'direction_angle' : direction_angle,
		'x': x, 'y': y, 'z': z, 'speed': speed,
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_position_by_id(str(id))

def remove_position(id):
	return remove(id, get_position_by_id, POSITIONS_COLLECTION_NAME)

def update_positions(**kwargs):
	return adjust_and_update(kwargs, POSITIONS_COLLECTION_NAME, None, None)

def select_positions(**kwargs):
	return select(kwargs, POSITIONS_COLLECTION_NAME)

# - sensor_data --------------------------------------------------------------------------------

def get_all_sensor_data():
    return get_all_items(SENSOR_DATA_COLLECTION_NAME)

# -- by id

def get_sensor_data_by_id(id):
    return get_item_by_id(SENSOR_DATA_COLLECTION_NAME, id)

# -- manipulators

def create_sensor_data(timestamp, source, event, meaning, value, units):
	id = db[SENSOR_DATA_COLLECTION_NAME].insert({'timestamp': timestamp, 'source': ObjectId(source), 'event': event,
		'meaning': meaning, 'value': value, 'units': units, 
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_sensor_data_by_id(str(id))

def remove_sensor_data(id):
	return remove(id, get_sensor_data_by_id, SENSOR_DATA_COLLECTION_NAME)

def update_sensor_data(**kwargs):
	return adjust_and_update(kwargs, SENSOR_DATA_COLLECTION_NAME, None, None)

def select_sensor_data(**kwargs):
	return select(kwargs, SENSOR_DATA_COLLECTION_NAME)

# - shift_state --------------------------------------------------------------------------------

def get_all_shift_states():
    return get_all_items(SHIFT_STATES_COLLECTION_NAME)

# -- by id

def get_shift_state_by_id(id):
    return get_item_by_id(SHIFT_STATES_COLLECTION_NAME, id)

# -- manipulators

def create_shift_state(timestamp, shift, warninglevel, cartridges, air, electricity, comment):
	id = db[SHIFT_STATES_COLLECTION_NAME].insert({'timestamp': timestamp, 'shift': ObjectId(shift), 'warning_level': warninglevel,
		'air': air, 'electricity': electricity, 'cartridges': cartridges, 'comment': comment, 
		'__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_shift_state_by_id(str(id))

def remove_shift_state(id):
	return remove(id, get_shift_state_by_id, SHIFT_STATES_COLLECTION_NAME)

def update_shift_states(**kwargs):
	return adjust_and_update(kwargs, SHIFT_STATES_COLLECTION_NAME, None, None)

def select_shift_states(**kwargs):
	return select(kwargs, SHIFT_STATES_COLLECTION_NAME)

# - operation_state ----------------------------------------------------------------------------

def get_all_operation_states():
    return get_all_items(OPERATION_STATES_COLLECTION_NAME)

# -- by id

def get_operation_state_by_id(id):
    return get_item_by_id(OPERATION_STATES_COLLECTION_NAME, id)

# -- manipulators

def create_operation_state(timestamp, boat, operation, status, distance, zenith, azimuth, hydrogenium, helium, lithium, beryllium, borum,\
    carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,\
    scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,\
    crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,\
    stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,\
    terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,\
    hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,\
    plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,\
    seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,\
    oganesson, comment):
	id = db[OPERATION_STATES_COLLECTION_NAME].insert({'timestamp': timestamp, 'boat': ObjectId(boat), 'operation': ObjectId(operation),
		'status': status, 'distance': distance, 'zenith': zenith, 'azimuth': azimuth,
		'hydrogenium': hydrogenium, 'helium': helium, 'lithium': lithium, 'beryllium': beryllium, 'borum': borum, 
		'carboneum': carboneum, 'nitrogenium': nitrogenium, 'oxygenium': oxygenium, 'fluorum': fluorum, 'neon': neon, 
		'natrium': natrium, 'magnesium': magnesium, 'aluminium': aluminium, 'silicium': silicium, 'phosphorus': phosphorus, 'sulfur': sulfur,
		'chlorum': chlorum, 'argon': argon, 'kalium': kalium, 'calcium': calcium, 'scandium': scandium, 'titanium': titanium, 'vanadium': vanadium, 
		'chromium': chromium, 'manganum': manganum, 'ferrum': ferrum, 'cobaltum': cobaltum, 'niccolum': niccolum, 'cuprum': cuprum, 'zincum': zincum,
		'gallium': gallium, 'germanium': germanium, 'arsenicum': arsenicum, 'selenium': selenium, 'bromum': bromum, 'crypton': crypton, 'rubidium': rubidium,
		'strontium': strontium, 'yttrium': yttrium, 'zirconium': zirconium, 'niobium': niobium, 'molybdaenum': molybdaenum, 'technetium': technetium, 
		'ruthenium': ruthenium, 'rhodium': rhodium, 'palladium': palladium, 'argentum': argentum, 'cadmium': cadmium, 'indium': indium, 
		'stannum': stannum, 'stibium': stibium, 'tellurium': tellurium, 'iodium': iodium, 'xenon': xenon, 'caesium': caesium, 'barium': barium, 
		'lanthanum': lanthanum, 'cerium': cerium, 'praseodymium': praseodymium, 'neodymium': neodymium, 'promethium': promethium, 
		'samarium': samarium, 'europium': europium, 'gadolinium': gadolinium, 'terbium': terbium, 'dysprosium': dysprosium, 
		'holmium': holmium, 'erbium': erbium, 'thulium': thulium, 'ytterbium': ytterbium, 'lutetium': lutetium, 'hafnium': hafnium, 
		'tantalum': tantalum, 'wolframium': wolframium, 'rhenium': rhenium, 'osmium': osmium, 'iridium': iridium, 'platinum': platinum, 
		'aurum': aurum, 'hydrargyrum': hydrargyrum, 'thallium': thallium, 'plumbum': plumbum, 'bismuthum': bismuthum, 'polonium': polonium, 
		'astatum': astatum, 'radon': radon, 'francium': francium, 'radium': radium, 'actinium': actinium, 'thorium': thorium, 
		'protactinium': protactinium, 'uranium': uranium, 'neptunium': neptunium, 'plutonium': plutonium, 'americium': americium, 'curium': curium, 
		'berkelium': berkelium, 'californium': californium, 'einsteinium': einsteinium, 'fermium': fermium, 'mendelevium': mendelevium, 'nobelium': nobelium, 
		'lawrencium': lawrencium, 'rutherfordium': rutherfordium, 'dubnium': dubnium, 'seaborgium': seaborgium, 'bohrium': bohrium, 'hassium': hassium, 
		'meitnerium': meitnerium, 'darmstadtium': darmstadtium, 'roentgenium': roentgenium, 'copernicium': copernicium, 'nihonium': nihonium, 
		'flerovium': flerovium, 'moscovium': moscovium, 'livermorium': livermorium, 'tennessium': tennessium, 'oganesson': oganesson,
		'comment': comment, '__created__': datetime.datetime.now(), '__accessed__': datetime.datetime.now(), '__gaps__': [0]})
	return get_operation_state_by_id(str(id))

def remove_operation_state(id):
	return remove(id, get_operation_state_by_id, OPERATION_STATES_COLLECTION_NAME)

def update_operation_states(**kwargs):
	return adjust_and_update(kwargs, OPERATION_STATES_COLLECTION_NAME, None, None)

def select_operation_states(**kwargs):
	return select(kwargs, OPERATION_STATES_COLLECTION_NAME)

if __name__ == '__main__':
	print(update_people(name = 'dima', set_name = 'dimas'))
	#print(select_sensor(name = 'o'))
	#print(create_location('test loc'))
	#print(get_all_properties())
	#print(get_people_ids_with_spec('5ac52207cc314386b6f43441'))
	#print(get_all_property_types())
	#print(get_all_ids('system_test'))