from py2neo import Graph
import datetime
import configparser
import os, sys, re
from neomodel import config

configp = configparser.ConfigParser()
configp.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

NEO4J_DB_URL = os.environ.get('NEO4J_DB_URL') or configp['NEO4J']['host']
NEO4J_DB_PORT = int(os.environ.get('NEO4J_DB_PORT') or configp['NEO4J']['port'])

USERNAME = os.environ.get('NEO4J_DB_USERNAME') or configp['NEO4J']['username']
PASSWORD = os.environ.get('NEO4J_DB_PASSWORD') or configp['NEO4J']['password']

graph = Graph(bolt = True, user = USERNAME, password = PASSWORD, host = NEO4J_DB_URL, http_port = NEO4J_DB_PORT)

config.DATABASE_URL = 'bolt://' + USERNAME + ':' + PASSWORD + '@' + NEO4J_DB_URL + ':' + str(NEO4J_DB_PORT)

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations/entities')

from shift import Shift
from person import Person
from department import Department
from operation import Operation
from requirement import Requirement

def get_operation_ids_by_requirement(requirement_id):
	return [\
		item['ident'] for item in graph.data("""
			match (r:Requirement)-[:USER]->(o:Operation)
			where r.ident = '%s'
			return o.ident as ident
			""" % requirement_id)]

def get_shift_ids_by_requirement(requirement_id):
	return [\
		item['ident'] for item in graph.data("""
			match (r:Requirement)-[:USER]->(s:Shift)
			where r.ident = '%s'
			return s.ident as ident
			""" % requirement_id)]


#

def get_operation_requirements_id(operation_id):
	return [\
		item['ident'] for item in graph.data("""
			match (r:Requirement)-[:USER]->(o:Operation)
			where o.ident = '%s'
			return r.ident as ident
			""" % operation_id)]

def get_shift_requirements_id(shift_id):
	return [\
		item['ident'] for item in graph.data("""
			match (r:Requirement)-[:USER]->(s:Shift)
			where s.ident = '%s'
			return r.ident as ident
			""" % shift_id)]



def int_to_mongo_str_id(value):
	return (value).to_bytes(12, byteorder='big').hex()

def mongo_str_id_to_int(value):
	return int.from_bytes(bytearray.fromhex(' '.join(re.findall('..', value))), 'big')

def get_name_by_id(label, id):
	#print([item for item in graph.data("MATCH (item:%s) WHERE item.ident = '%s' RETURN item.ident" % (label, id))])
	return [item['item.name'] for item in graph.data("MATCH (item:%s) WHERE item.ident = '%s' RETURN item.name" % (label, id))][0]

def get_operation_head_id(operation_id):
	return [\
		item['ident'] for item in graph.data("""
			match (p:Person)-[:HEAD]->(o:Operation)
			where o.ident = '%s'
			return space_ship.get_hex_ident(p.ident) as ident
			""" % operation_id)][0]

def get_headed_operations(person_id):
	return [\
		item for item in graph.data("""
			match (p:Person)-[:HEAD]->(o:Operation)
			where space_ship.get_hex_ident(p.ident) = '%s'
			return o.ident as ident, o.start as start, o.end as end, o.name as name
			""" % person_id)]

def get_directed_ids(person_id):
	return [\
		item['ident'] for item in graph.data("""
			match (p:Person)-[:DIRECTOR]->(d:Department)
			where space_ship.get_hex_ident(p.ident) = '%s'
			return space_ship.get_hex_ident(d.ident) as ident
			""" % person_id)]

def get_director_id(department_id):
	return [\
		item['ident'] for item in graph.data("""
			match (p:Person)-[:DIRECTOR]->(d:Department)
			where space_ship.get_hex_ident(d.ident) = '%s'
			return space_ship.get_hex_ident(p.ident) as ident
			""" % department_id)][0]

def get_chiefed_shifts(person_id):
	return [\
		item for item in graph.data("""
			match (p:Person)-[:CHIEF]->(s:Shift)
			where space_ship.get_hex_ident(p.ident) = '%s'
			return s.ident as ident, s.start as start, s.end as end
			""" % person_id)]

def get_executed_operations(person_id):
	return [\
		item for item in graph.data("""
			match (p:Person)-[:EXECUTOR]->(o:Operation)
			where space_ship.get_hex_ident(p.ident) = '%s'
			return o.ident as ident, o.start as start, o.end as end, o.name as name
			""" % person_id)]

def get_worked_shifts(person_id):
	return [\
		item for item in graph.data("""
			match (p:Person)-[:WORKER]->(s:Shift)
			where space_ship.get_hex_ident(p.ident) = '%s'
			return s.ident as ident, s.start as start, s.end as end
			""" % person_id)]

def get_shift_chief_id(shift_id):
	return [\
		item['ident'] for item in graph.data("""
			match (p:Person)-[:CHIEF]->(s:Shift)
			where s.ident = '%s'
			return space_ship.get_hex_ident(p.ident) as ident
			""" % shift_id)][0]

def get_executors_id(operation_id):
	return [\
		item['ident'] for item in graph.data("""
			match (p:Person)-[:EXECUTOR]->(o:Operation)
			where o.ident = '%s'
			return space_ship.get_hex_ident(p.ident) as ident
			""" % operation_id)]

def get_workers_id(shift_id):
	return [\
		item['ident'] for item in graph.data("""
			match (p:Person)-[:WORKER]->(s:Shift)
			where s.ident = '%s'
			return space_ship.get_hex_ident(p.ident) as ident
			""" % shift_id)]
	

def get_all_ids(label):
	return [item['item.ident'] for item in graph.data("MATCH (item:%s) RETURN item.ident" % label)]

def is_valid_foreign_id(label, id):
	return id in get_all_ids(label)

####

ID_DELIMITER = ','
REQ_COMPONENT_DELIMITER = ':'

def ensure_person_existance(person_id):
	if not len(graph.data("match (p:Person) where space_ship.get_hex_ident(p.ident) = '%s' return p.ident as ident" % person_id)) > 0:
		Person(ident = person_id).save()

def ensure_department_existance(department_id):
	if not len(graph.data("match (d:Department) where space_ship.get_hex_ident(d.ident) = '%s' return d.ident as ident" % department_id)) > 0:
		Department(ident = department_id).save()

def ensure_requirement_existance(requirement_id):
	if not len(graph.data("match (r:Requirement) where r.ident = '%s' return r.ident as ident" % requirement_id)) > 0:
		raise ValueError('requirement not exists')

def add_worker(shift_id, worker_id):
	graph.data("""match (p:Person), (s:Shift) 
				  where space_ship.get_hex_ident(p.ident) = '%s' and
                  s.ident = '%s'
                  create (p)-[:WORKER]->(s)
                  return s.ident as ident;""" % (worker_id, shift_id))

def add_shift_requirement(shift_id, requirement_id):
	graph.data("""match (r:Requirement), (s:Shift) 
				  where r.ident = '%s' and
                  s.ident = '%s'
                  create (r)-[:USER]->(s)
                  return s.ident as ident;""" % (requirement_id, shift_id))

def set_chief(shift_id, chief_id):
	graph.data("""match (p:Person), (s:Shift) 
				  where space_ship.get_hex_ident(p.ident) = '%s' and
                  s.ident = '%s'
                  create (p)-[:CHIEF]->(s)
                  return s.ident as ident;""" % (chief_id, shift_id))

def set_shift_department(shift_id, department_id):
	graph.data("""match (d:Department), (s:Shift) 
				  where space_ship.get_hex_ident(d.ident) = '%s' and
                  s.ident = '%s'
                  create (s)-[:INCORPORATION]->(d)
                  return s.ident as ident;""" % (department_id, shift_id))

def create_shift(chief, department, start, end, workers, requirements):
	new_shift = Shift(start = start, end = end).save()
	
	for person_id in workers.split(ID_DELIMITER):
		ensure_person_existance(person_id)
		add_worker(new_shift.ident, person_id)

	for requirement_id in requirements.split(ID_DELIMITER):
		ensure_requirement_existance(requirement_id)
		add_shift_requirement(new_shift.ident, requirement_id)

	ensure_person_existance(chief)
	set_chief(new_shift.ident, chief)

	ensure_department_existance(department)
	set_shift_department(new_shift.ident, department)

	return new_shift

def remove_shift(ident):
	deleted = Shift.nodes.get(ident = ident)
	graph.data("""match (s:Shift) where s.ident = '%s' detach delete s""" % ident)
	return deleted

#

def add_executor(operation_id, executor_id):
	graph.data("""match (p:Person), (o:Operation) 
				  where space_ship.get_hex_ident(p.ident) = '%s' and
                  o.ident = '%s'
                  create (p)-[:EXECUTOR]->(o)
                  return o.ident as ident;""" % (executor_id, operation_id))

def add_operation_requirement(operation_id, requirement_id):
	graph.data("""match (r:Requirement), (o:Operation) 
				  where r.ident = '%s' and
                  o.ident = '%s'
                  create (r)-[:USER]->(o)
                  return o.ident as ident;""" % (requirement_id, operation_id))

def set_head(operation_id, head_id):
	graph.data("""match (p:Person), (o:Operation) 
				  where space_ship.get_hex_ident(p.ident) = '%s' and
                  o.ident = '%s'
                  create (p)-[:HEAD]->(o)
                  return o.ident as ident;""" % (head_id, operation_id))

def create_operation(name, head, start, end, executors, requirements):
	new_operation = Operation(name = name, start = start, end = end).save()
	
	for person_id in executors.split(ID_DELIMITER):
		ensure_person_existance(person_id)
		add_executor(new_operation.ident, person_id)

	for requirement_id in requirements.split(ID_DELIMITER):
		ensure_requirement_existance(requirement_id)
		add_operation_requirement(new_operation.ident, requirement_id)

	ensure_person_existance(head)
	set_head(new_operation.ident, head)

	return new_operation

def remove_operation(ident):
	deleted = Operation.nodes.get(ident = ident)
	graph.data("""match (o:Operation) where o.ident = '%s' detach delete o""" % ident)
	return deleted

#

def create_requirement(name, content):
	requirement_parts = []
	
	for requirement_str_part in content.split(ID_DELIMITER):
		specialization, quantity = requirement_str_part.split(REQ_COMPONENT_DELIMITER)
		requirement_parts.append({'ident' : specialization, 'quantity' : quantity})

	return Requirement(name = name, content = requirement_parts).save()

def remove_requirement(ident):
	deleted = Requirement.nodes.get(ident = ident)
	graph.data("""match (r:Requirement) where r.ident = '%s' detach delete r""" % ident)
	return deleted

#

#

#

def select_operations(**kwargs):
	return [item for item in Operation.nodes.filter(**{arg : kwargs[arg] for arg in kwargs if kwargs[arg]})]

if __name__ == '__main__':
	print(select_operations(name__iregex = '.*.*'))
	#print(is_valid_foreign_id('Shift', 'a983d357069f4363803f87b5cc7c8f7d'))
	
	#create_requirement('good team', '5ac52207cc314386b6f43441:13,5ac5220ccc314386b6f43442:17')
	
	#remove_requirement('0ac5f860d78841cfb9afbb61315baa5d')

	#remove_operation('05e36fbdcd7c4bd5b488ebe7729ddb9d')

	#create_operation('Explore space', '5ad22dbfd678f46fc1059829', datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days = 2), 
	#	'5ac8a5791767171855a9dd8a,5ac8a57c1767171855a9dd8b,5ad234cdd678f476d7f5971c','b9515d6075074c3fa6284ea6d796847f')

	#remove_shift('3b72400560fd44be81facc4480d99e72')
	
	#create_shift('5ad22dbfd678f46fc1059829', '5ad22660d678f46b00afe113', datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days = 2), 
	#	'5ac8a5791767171855a9dd8a,5ac8a57c1767171855a9dd8b,5ad234cdd678f476d7f5971c','b9515d6075074c3fa6284ea6d796847f')

#

#int.from_bytes(bytearray.fromhex(' '.join(re.findall('..', '5abfdba6ee6b7f5eec83a1ca'))), 'big')

#/api/create/shift/fields=ok&where=chief:'5ad22dbfd678f46fc1059829',department:'5ad22660d678f46b00afe113',start:'2017-02-12 23:59:59',end:'2017-02-17 23:59:59',workers:'5ac8a5791767171855a9dd8a,5ac8a57c1767171855a9dd8b,5ad234cdd678f476d7f5971c',requirements:'b9515d6075074c3fa6284ea6d796847f'
#/api/create/operation/fields=ok&where=name:'Prometheus',head:'5ad33da1d678f4590ebcebd2',start:'2017-02-12 23:59:59',end:'2017-02-17 23:59:59',workers:'5ac8a5791767171855a9dd8a,5ac8a57c1767171855a9dd8b,5ad234cdd678f476d7f5971c',requirements:'b9515d6075074c3fa6284ea6d796847f'
#/api/create/operation/fields=ok&where=name:'good team',content:'5ac52207cc314386b6f43441:13,5ac5220ccc314386b6f43442:17'