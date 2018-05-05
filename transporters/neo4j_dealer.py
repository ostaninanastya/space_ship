import sys, os, datetime
from bson.objectid import ObjectId
import configparser
import pickle

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations/adapters/')
from mongo_adapter import mongo_str_id_to_int, int_to_mongo_str_id

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations/adapters/')
from mongo_adapter import mongo_str_id_to_int

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']
TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

## Convert stringified list back to list 
def string_to_list(strlist):
	return [float(item.lstrip().rstrip()) for item in strlist.replace('[','').replace(']','').split(',')]

## Convert item's property from mongo format to cassandra query format
def stringify(value):
	#print(type(value))
	if isinstance(value, datetime.datetime):
		return '\'' + value.strftime(TIMESTAMP_PATTERN) + '\''
	elif isinstance(value, int) or isinstance(value, float) or isinstance(value, list):
		return str(value)
	elif isinstance(value, ObjectId):
		return  str(list(mongo_str_id_to_int(str(value))))
	elif isinstance(value, bytes):
		return  str(list(mongo_str_id_to_int(value.hex())))
	return '\'' + str(value) + '\''

## Convert item from mongo format to neo4j query format
def querify(item, prefix = '', delimiter = ' : ', field_delimiter = ' and ', with_where = True):
	querified = []
	for key in item:
		if item[key]:
			querified.append([key, stringify(item[key])])

	criterias = [prefix + item[0] + delimiter + item[1] for item in querified]
	joined_criterias = field_delimiter.join(criterias)
	return 'where {0} '.format(joined_criterias) if len(criterias) > 0 and with_where else joined_criterias

## Convert item, came from neo4j, to mongo format
def repair(item):
	repaired = {}
	for key in dict(item):
		value = item[key]
		if key == '_id' or key in ['location', 'state', 'supervisor', 'type', 'department', 'specialization', 'director']:
			value = ObjectId(item[key])
		else:
			try:
				value = datetime.datetime.strptime(value, TIMESTAMP_PATTERN)
			except:
				if key in ['n.location', 'n.state', 'n.supervisor', 'n.type', 'n.department', 'n.specialization', 'n.director']:
					#print('==================================================',value)
					value = ObjectId(int_to_mongo_str_id(value))
				pass
		repaired[key.replace('n.', '')] = value

	#print('-----',repaired)

	return repaired