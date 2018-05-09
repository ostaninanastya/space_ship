import sys, os, datetime, math
from bson.objectid import ObjectId
import configparser
import pickle

def isfloat(value):
    try: 
        float(str(value))
    except ValueError: 
        return False
    return not isinstance(value, ObjectId)

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations/adapters/')
from mongo_adapter import mongo_str_id_to_int, int_to_mongo_str_id

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/relations/adapters/')
from mongo_adapter import mongo_str_id_to_int

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']
TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

def string_to_requirement_entry(strset):
	fields = [item.lstrip().rstrip() for item in strset.replace('{','').replace('}','').replace('"','').split(',')]
	specialization = ObjectId(fields[0].split(':')[1].lstrip().rstrip().replace('id',''))
	quantity = int(fields[1].split(':')[1].lstrip().rstrip())
	return {'specialization': specialization, 'quantity': quantity}
			

## Convert stringified list back to list 
def string_to_list(strlist):
	try:
		return [float(item.lstrip().rstrip()) for item in strlist.replace('[','').replace(']','').split(',')]
	except:
		try:
			return [ObjectId(item.lstrip().rstrip().replace('id','')) for item in strlist]
		except:
			return [string_to_requirement_entry(item.lstrip().rstrip()) for item in strlist]

## Convert item's property from mongo format to cassandra query format
def stringify(value, embedded = False):
	#print(type(value))
	if isinstance(value, datetime.datetime):
		return '\'' + value.strftime(TIMESTAMP_PATTERN) + '\''
	elif isinstance(value, int) or isinstance(value, float):
		return str(value)
	elif isinstance(value, dict):
		return ('\"{' + ', '.join([key + ': ' + stringify(value[key], embedded = True).replace('\'','') for key in value]) + '}\"')
	elif isinstance(value, list):
		return str([stringify(item, embedded = True) for item in value]).replace('\'','')
	elif isinstance(value, ObjectId):
		if not embedded:
			return str(list(mongo_str_id_to_int(str(value))))
		else:
			return '\'' + 'id' + str(value) + '\''
	elif isinstance(value, bytes):
		return  '\'' + value.hex() + '\''
	return '\'' + str(value) + '\''

## Convert item from mongo format to neo4j query format
def querify(item, prefix = '', delimiter = ' : ', field_delimiter = ' and ', with_where = True):
	querified = []
	for key in item:
		if (item[key] or (isfloat(item[key]) and item[key] == 0)) and (not isfloat(item[key]) or not math.isnan(item[key])):
			querified.append([key, stringify(item[key])])

	criterias = [prefix + item[0] + delimiter + item[1] for item in querified]
	joined_criterias = field_delimiter.join(criterias)
	return 'where {0} '.format(joined_criterias) if len(criterias) > 0 and with_where else joined_criterias

## Convert item, came from neo4j, to mongo format
def repair(item):
	repaired = {}
	for key in dict(item):
		value = item[key]
		if key == 'n.workers' or key == 'n.requirements' or key == 'n.executors' or key == 'n.content':
			value = string_to_list(value)
		elif key == '_id' or key in ['location', 'state', 'supervisor', 'type', 'department', 'specialization', 'director', 'chief', 'head',
									'shift', 'operation', 'user', 'system', 'source', 'boat']:
			value = ObjectId(item[key])
		else:
			try:
				value = datetime.datetime.strptime(value, TIMESTAMP_PATTERN)
			except:
				if key in ['n.location', 'n.state', 'n.supervisor', 'n.type', 'n.department', 'n.specialization', 'n.director', 'n.chief', 'n.head',
							'n.shift', 'n.operation', 'n.user', 'n.system', 'n.source', 'n.boat']:
					#print('==================================================',value)
					value = ObjectId(int_to_mongo_str_id(value))
				if key in ['n.mac_address']:
					#print('==================================================',value)
					value = bytes.fromhex(value)
				pass
		repaired[key.replace('n.', '')] = value

	#print('-----',repaired)

	return repaired