from pymongo import MongoClient
import configparser
import os, re

from bson.objectid import ObjectId

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

MONGO_DB_URL = os.environ.get('MONGO_DB_URL') if os.environ.get('MONGO_DB_URL') else config['MONGO']['host']
MONGO_DB_PORT = int(os.environ.get('MONGO_DB_PORT') if os.environ.get('MONGO_DB_PORT') else config['MONGO']['port'])
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') if os.environ.get('MONGO_DB_NAME') else config['MONGO']['db_name']

db = MongoClient(MONGO_DB_URL, MONGO_DB_PORT)[MONGO_DB_NAME]

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

def get_sensors_by_location_id(location_id):
	location_object_id = ObjectId(location_id)
	return [item for item in db['source_test'].find({'location' : location_object_id})]

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

def get_sensor_by_id(id):
    return get_item_by_id('source_test', id)

def get_system_state_by_id(id):
    return get_item_by_id('system_state_test', id)

def get_system_type_by_id(id):
    return get_item_by_id('system_types_test', id)

def get_system_by_id(id):
    return get_item_by_id('sys_test', id)

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

##

def create_location(name):
	id = db['location_test'].insert({'name' : name})
	return get_location_by_id(str(id))

def remove_location(id):
	deleted = get_location_by_id(str(id))
	id = db['location_test'].delete_one({'_id' : ObjectId(id)})
	return deleted


###

if __name__ == '__main__':
	print(create_location('test loc'))
	#print(get_all_properties())
	#print(get_people_ids_with_spec('5ac52207cc314386b6f43441'))
	#print(get_all_property_types())
	#print(get_all_ids('system_test'))