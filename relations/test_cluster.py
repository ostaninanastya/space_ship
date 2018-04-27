import os,sys
import json

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/connectors')

from py2neo import Graph
from neo4j_connector import connect

def main():

	try:
		conn = connect()
		graph = Graph(bolt = True, user = conn['username'], password = conn['password'], host = conn['host'], bolt_port = conn['port'])
		graph.begin()
	except:
		print('Connection is not set')
	else:
		print('Connection is set')

		try:
			graph.data("MATCH (n) RETURN 1;")
		except:
			print('Select query is not resolved')
		else:
			print('Select query is resolved')

if __name__ == '__main__':
	main()


