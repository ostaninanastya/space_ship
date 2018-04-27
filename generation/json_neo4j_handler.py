import sys, os
import json
from pprint import pprint
import datetime
import configparser
import time

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/adapters')

from mongo_adapter import mongo_str_id_to_int

renaming = {'system' : 'system_id', 'sensor_id' : 'source_id'}

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']


#


from py2neo import Graph

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/connectors')
from neo4j_connector import connect_to_leader

conn = connect_to_leader()
graph = Graph(bolt = True, user = conn['username'], password = conn['password'], host = conn['host'], bolt_port = conn['port'])

def try_to_repair(key, value, mongo_ids, neo_ids, strings):
	if key in mongo_ids:
		return "0x" + int(value).to_bytes(12, byteorder='big').hex()
	if key in neo_ids:
		return "0x" + int(value).to_bytes(16, byteorder='big').hex()
	if key == "time" and len(value) == 5:
		return value + ":00"
	if key == "mac_address":
		return "0x" + abs(int(value)).to_bytes(6, byteorder='big').hex()
	if key in strings:
		return value
	try:
		floated = float(value)
		if floated - int(floated) == 0:
			return int(floated)
		return floated
	except:
		return value

def validate_key(key):
	if key in renaming:
		return renaming[key]
	return key

def str_mongo_id_to_internal_repr(value):
	return list(mongo_str_id_to_int(int(value).to_bytes(12, byteorder='big').hex()))

def str_id_to_internal_repr(value):
	return int(value).to_bytes(16, byteorder='big').hex()

def str_date_to_internal_repr(value):
	return datetime.datetime.strptime(value, DATE_PATTERN).timestamp()

def create_node(label, properties):
	query = "CREATE (n:{0} {1});".format(label, str(properties)).replace('\':',':').replace(', \'', ', ').replace('{\'','{')
	try:
		#print(query)
		graph.data(query)
	except:
		print('{0} with {1} exists'.format(label, properties))
	return query

def create_connected_node(label, properties, connection_label, destination_label, destination_id, destination_id_field, source_id_field, auto_create = True):
	if auto_create:
		create_node(label, properties)
	query = 'match (s:{0}), (d:{1}) where not (s)-[:{4}]->(d) and d.{2} = {3} and s.{5} = {6} create (s)-[:{4}]->(d);'.format(label, destination_label, destination_id_field, destination_id, connection_label, source_id_field, properties[source_id_field])
	graph.data(query)
	return query


def str_to_int_array(strarr):
	return [int(item) for item in strarr.replace('[','').replace(']','').split(', ')]

def import_operations(filepath, base):
	counter = 0
	scalar = ["name"]
	ids = ["ident"]
	mongo_ids = ["head"]
	dates = ["start", "end"]

	data = json.load(open(filepath))

	result = {"data" : []}

	counter = 0

	for item in data[base]:
		result["data"].append({ key : item[key] for key in item if key in scalar})

	for key in ids:
		for i in range(len(data[base])):
			result["data"][i][key] = str_id_to_internal_repr(data[base][i][key])

	#for key in mongo_ids:
	#	for i in range(len(data[base])):
	#		result["data"][i][key] = str_mongo_id_to_internal_repr(data[base][i][key])

	for key in dates:
		for i in range(len(data[base])):
			result["data"][i][key] = str_date_to_internal_repr(data[base][i][key])


	for item in result["data"]:
		print(counter, ' operations created')
		create_node("Operation", item)
		counter += 1

	counter = 0
	for item in data[base]:
		print(counter, ' requirements processed')
		for id in str_to_int_array(item['persons']):
			create_connected_node('Person', {'ident': str_mongo_id_to_internal_repr(id)}, 'EXECUTOR', 'Operation', '\'' + str_id_to_internal_repr(item['ident']) + '\'', 'ident', 'ident')

		create_connected_node('Person', {'ident': str_mongo_id_to_internal_repr(item['head'])}, 'HEAD', 'Operation', '\'' + str_id_to_internal_repr(item['ident']) + '\'', 'ident', 'ident')
		create_connected_node('Department', {'ident': str_mongo_id_to_internal_repr(item['department'])}, 'INCORPORATION', 'Operation', '\'' + str_id_to_internal_repr(item['ident']) + '\'', 'ident', 'ident')
		counter += 1
	return "ok"

def import_shifts(filepath, base):
	counter = 0
	scalar = []
	ids = ["ident"]
	mongo_ids = ["head"]
	dates = ["start", "end"]

	data = json.load(open(filepath))

	result = {"data" : []}

	counter = 0

	for item in data[base]:
		result["data"].append({ key : item[key] for key in item if key in scalar})

	for key in ids:
		for i in range(len(data[base])):
			result["data"][i][key] = str_id_to_internal_repr(data[base][i][key])

	#for key in mongo_ids:
	#	for i in range(len(data[base])):
	#		result["data"][i][key] = str_mongo_id_to_internal_repr(data[base][i][key])

	for key in dates:
		for i in range(len(data[base])):
			result["data"][i][key] = str_date_to_internal_repr(data[base][i][key])


	for item in result["data"]:
		print(counter, ' shifts created')
		create_node("Shift", item)
		counter += 1

	counter = 0
	for item in data[base]:
		print(counter, ' shifts processed')
		for id in str_to_int_array(item['persons']):
			create_connected_node('Person', {'ident': str_mongo_id_to_internal_repr(id)}, 'WORKER', 'Shift', '\'' + str_id_to_internal_repr(item['ident']) + '\'', 'ident', 'ident')

		create_connected_node('Person', {'ident': str_mongo_id_to_internal_repr(item['head'])}, 'CHIEF', 'Shift', '\'' + str_id_to_internal_repr(item['ident']) + '\'', 'ident', 'ident')
		create_connected_node('Department', {'ident': str_mongo_id_to_internal_repr(item['department'])}, 'INCORPORATION', 'Shift', '\'' + str_id_to_internal_repr(item['ident']) + '\'', 'ident', 'ident')
		counter += 1
	return "ok"

def import_departments(filepath, base):
	data = json.load(open(filepath))

	counter = 0
	for item in data[base]:
		print(counter, ' departments created')
		counter += 1
		create_node("Department", {'ident' : str_mongo_id_to_internal_repr(item['ident'])})
		create_connected_node('Person', {'ident': str_mongo_id_to_internal_repr(item['controller'])}, 'DIRECTOR', 'Department', str_mongo_id_to_internal_repr(item['ident']), 'ident', 'ident')

	return "ok"

def import_requirements(filepath, base):
	data = json.load(open(filepath))

	counter = 0
	for item in data[base]:
		print(counter, ' requirements created')
		create_node('Requirement', {'name' : item['name'], 'ident' : str_id_to_internal_repr(item['ident']), 'content' : [str({'specialization' : str_mongo_id_to_internal_repr(item['content']['ident']), 'quantity' : item['content']['quantity']}).replace('\'','"')]})
		for operation in item['operations']:
			create_connected_node('Requirement', 
			{'ident': '\'' + str_id_to_internal_repr(item['ident']) + '\''}, 'USER', 'Operation',
			 '\'' + str_id_to_internal_repr(operation) + '\'', 'ident', 'ident', auto_create = False)

		for shift in item['shifts']:
			create_connected_node('Requirement', 
			{'ident': '\'' + str_id_to_internal_repr(item['ident']) + '\''}, 'USER', 'Shift',
			 '\'' + str_id_to_internal_repr(shift) + '\'', 'ident', 'ident', auto_create = False)
		#print(counter, ' created')
		counter += 1
		#create_node("Department", {'ident' : str_id_to_internal_repr(item['ident'])})


	return "ok"

if __name__ == '__main__':
	direction = sys.argv[1]
	
	if not direction or direction == 'departments':
		import_departments(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/neo4j json/department.json', 'department')
	if not direction or direction == 'shifts':
		import_shifts(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/neo4j json/shift.json', 'shift')
	if not direction or direction == 'operations':
		import_operations(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/neo4j json/operation.json', 'operation')
	if not direction or direction == 'requirements':
		import_requirements(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/neo4j json/requirement.json', 'requirements')
	
	start = time.time()
	
	print('took ', time.time() - start)
	#print(import_departments(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/neo4j json/department.json', 'department'))
	#print(import_operations(os.environ['SPACE_SHIP_HOME'] + '/generation/dummyMarket/neo4j json/operation.json', 'operation'))