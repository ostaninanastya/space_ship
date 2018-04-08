from py2neo import Graph

import configparser
import os, sys, re

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

NEO4J_DB_URL = os.environ.get('NEO4J_DB_URL') if os.environ.get('NEO4J_DB_URL') else config['NEO4J']['host']
NEO4J_DB_PORT = int(os.environ.get('NEO4J_DB_PORT') if os.environ.get('NEO4J_DB_PORT') else config['NEO4J']['port'])

USERNAME = os.environ.get('NEO4J_DB_USERNAME') if os.environ.get('NEO4J_DB_USERNAME') else config['NEO4J']['username']
PASSWORD = os.environ.get('NEO4J_DB_PASSWORD') if os.environ.get('NEO4J_DB_PASSWORD') else config['NEO4J']['password']

graph = Graph(bolt = True, user = USERNAME, password = PASSWORD, host = NEO4J_DB_URL, http_port = NEO4J_DB_PORT)


def int_to_mongo_str_id(value):
	return (value).to_bytes(12, byteorder='big').hex()

def mongo_str_id_to_int(value):
	return int.from_bytes(bytearray.fromhex(' '.join(re.findall('..', value))), 'big')

def get_name_by_id(label, id):
	#print([item for item in graph.data("MATCH (item:%s) WHERE item.ident = '%s' RETURN item.ident" % (label, id))])
	return [item['item.name'] for item in graph.data("MATCH (item:%s) WHERE item.ident = '%s' RETURN item.name" % (label, id))][0]

def get_operation_director_id(operation_id):
	return [\
		item['ident'] for item in graph.data("""
			match (p:Person)-[:DIRECTOR]->(o:Operation)
			where o.ident = '%s'
			return space_ship.get_hex_ident(p.ident) as ident
			""" % operation_id)][0]

def get_shift_chief_id(shift_id):
	return [\
		item['ident'] for item in graph.data("""
			match (p:Person)-[:CHIEF]->(s:Shift)
			where s.ident = '%s'
			return space_ship.get_hex_ident(p.ident) as ident
			""" % shift_id)][0]
	

def get_all_ids(label):
	return [item['item.ident'] for item in graph.data("MATCH (item:%s) RETURN item.ident" % label)]

def is_valid_foreign_id(label, id):
	return id in get_all_ids(label)

if __name__ == '__main__':
	print(is_valid_foreign_id('Shift', 'a983d357069f4363803f87b5cc7c8f7d'))


#int.from_bytes(bytearray.fromhex(' '.join(re.findall('..', '5abfdba6ee6b7f5eec83a1ca'))), 'big')