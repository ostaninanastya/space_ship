import os, sys
import configparser

from neomodel import config, db

configp = configparser.ConfigParser()
configp.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

NODE_DELIMITER = os.environ.get('HOST_DELIMITER') if os.environ.get('HOST_DELIMITER') else configp['NEO4J']['node_delimiter']

NEO4J_CORE_URLS = [item.split(':')[0].lstrip().rstrip() for item in 
	(os.environ.get('NEO4J_CORE_URLS') if os.environ.get('NEO4J_CORE_URLS') else configp['NEO4J']['core_nodes']).split(NODE_DELIMITER)]
NEO4J_CORE_PORTS = [int(item.split(':')[1].lstrip().rstrip()) for item in 
	(os.environ.get('NEO4J_CORE_PORTS') if os.environ.get('NEO4J_CORE_PORTS') else configp['NEO4J']['core_nodes']).split(NODE_DELIMITER)]

NEO4J_REPLICA_URLS = [item.split(':')[0].lstrip().rstrip() for item in 
	(os.environ.get('NEO4J_REPLICA_URLS') if os.environ.get('NEO4J_REPLICA_URLS') else configp['NEO4J']['read_replicas']).split(NODE_DELIMITER)]
NEO4J_REPLICA_PORTS = [int(item.split(':')[1].lstrip().rstrip()) for item in 
	(os.environ.get('NEO4J_REPLICA_PORTS') if os.environ.get('NEO4J_REPLICA_PORTS') else configp['NEO4J']['read_replicas']).split(NODE_DELIMITER)]

NEO4J_URLS = NEO4J_CORE_URLS + NEO4J_REPLICA_URLS 
NEO4J_PORTS =  NEO4J_CORE_PORTS + NEO4J_REPLICA_PORTS

USERNAME = os.environ.get('NEO4J_DB_USERNAME') if os.environ.get('NEO4J_DB_USERNAME') else configp['NEO4J']['username']
PASSWORD = os.environ.get('NEO4J_DB_PASSWORD') if os.environ.get('NEO4J_DB_PASSWORD') else configp['NEO4J']['password']

def connect_to_core(required_role = None):
	role = ''
	for replica_id in range(len(NEO4J_CORE_URLS)):
		try:
			db.set_connection('bolt://{0}:{1}@{2}:{3}/'.format(USERNAME, PASSWORD, NEO4J_CORE_URLS[replica_id], str(NEO4J_CORE_PORTS[replica_id])))
			role = db.cypher_query('call dbms.cluster.role();')[0][0][0]
		except:
			continue
		else:
			if (not role) or (required_role == role):
				return {'username': USERNAME, 'password': PASSWORD, 'host': NEO4J_CORE_URLS[replica_id], 'port': NEO4J_CORE_PORTS[replica_id]}
	
	raise Exception("Required core is disconnected")

def connect_to_leader():
	return connect_to_core(required_role = 'LEADER')

def connect_to_follower():
	return connect_to_core(required_role = 'FOLLOWER')

def connect():
	role = ''
	for replica_id in range(len(NEO4J_URLS)):
		try:
			config.DATABASE_URL = 'bolt://{0}:{1}@{2}:{3}/'.format(USERNAME, PASSWORD, NEO4J_URLS[replica_id], str(NEO4J_PORTS[replica_id]))
			role = db.cypher_query('call dbms.cluster.role();')[0][0][0]
		except:
			continue
		else:
			return {'username': USERNAME, 'password': PASSWORD, 'host': NEO4J_URLS[replica_id], 'port': NEO4J_PORTS[replica_id]}
	
	raise Exception("No active nodes")