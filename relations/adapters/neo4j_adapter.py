from py2neo import Graph
import configparser
import os, sys

config = configparser.ConfigParser()
config.read('../databases.config')

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/connectors')
from neo4j_connector import connect

conn = connect()
graph = Graph(bolt = True, user = conn['username'], password = conn['password'], host = conn['host'], bolt_port = conn['port'])

def int_to_mongo_str_id(value):
	return (value).to_bytes(12, byteorder='big').hex()

def mongo_str_id_to_int(value):
	return int.from_bytes(bytearray.fromhex(' '.join(re.findall('..', value))), 'big')

def is_valid_foreign_id(label, id):
	result = [item['item.ident'] for item in graph.data("MATCH (item:%s) RETURN item.ident" % label)]
	print(label)
	print(id)
	print(result)
	return id in result

if __name__ == '__main__':
	print(is_valid_foreign_id('Shift', 'a983d357069f4363803f87b5cc7c8f7d'))