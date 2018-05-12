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

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']
TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

## Convert stringified list back to list 
def string_to_list(strlist):
	return [float(item.lstrip().rstrip()) for item in strlist.replace('[','').replace(']','').split(',')]

## Convert item's property from mongo format to mysql query format
def stringify(value):
	if isinstance(value, datetime.datetime):
		return '\'' + value.strftime(TIMESTAMP_PATTERN) + '\''
	elif isinstance(value, list):
		return '0x' + pickle.dumps(value).hex()
	elif isinstance(value, int) or isinstance(value, float):
		return str(value)
	elif isinstance(value, ObjectId):
		return '0x' + str(value)
	elif isinstance(value, bytearray) or isinstance(value, bytes):
		return '0x' + value.hex()
	return '\'' + str(value) + '\''

## Convert item from mongo format to mysql query format
def querify(item, mode = 'INSERT', keys = None):
	querified = []
	for key in item:
		if (item[key] or (item[key] == 0)) and (not keys or key in keys) and (not isfloat(item[key]) or not math.isnan(item[key])):
			querified.append([key, stringify(item[key])])
			continue

	#print(querified)

	if mode == 'INSERT':
		return '(' + ', '.join([item[0] for item in querified]) + ') values (' + ', '.join([item[1] for item in querified]) + ')'
	elif mode == 'SELECT':
		criterias = [item[0] + ' = ' + item[1] for item in querified]
		joined_criterias = ', '.join(criterias)
		return 'where {0}'.format(joined_criterias) if len(criterias) > 0 else joined_criterias
	elif mode == 'DELETE':
		return ' and '.join([item[0] + ' = ' + item[1] for item in querified])

## Convert item, came from mysql, to mongo format
def repair(item, field_names):
	repaired = {}
	index = 0
	for key in field_names:
		if key == '__gaps__' or key == 'requirements' or key == 'workers' or key == 'executors' or key == 'content':
			#
			repaired[key] = pickle.loads(item[index])
		elif key == '_id' or key in ['location', 'state', 'supervisor', 'type', 'department', 'specialization', 'director', 'chief', 'head',
										'shift', 'operation', 'user', 'system', 'source', 'boat']:
			#print(item[index].hex())
			repaired[key] = ObjectId(item[index])
		else:
			repaired[key] = item[index]

		index += 1

	#print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',repaired)
					
	return repaired