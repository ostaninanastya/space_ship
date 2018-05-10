import sys, os, datetime, math
from bson.objectid import ObjectId
import configparser

def isfloat(value):
    try: 
        float(str(value))
    except ValueError: 
        return False
    return not isinstance(value, ObjectId)

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']
TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

def string_to_requirement_entry(strset):
	fields = [item.lstrip().rstrip() for item in strset.replace('{','').replace('}','').replace('"','').split(',')]
	specialization = ObjectId(fields[0].split(':')[1].lstrip().rstrip().replace('0x',''))
	quantity = int(fields[1].split(':')[1].lstrip().rstrip())
	return {'specialization': specialization, 'quantity': quantity}

## Convert stringified list back to list 
def string_to_list(strlist):
	#print(strlist)
	try:
		return [float(item.lstrip().rstrip()) for item in strlist.replace('[','').replace(']','').split(',')]
	except:
		try:
			return [ObjectId(item.lstrip().rstrip().replace('0x','')) for item in strlist.replace('[','').replace(']','').split(',')]
		except:
			return [string_to_requirement_entry(item.lstrip().rstrip()) for item in strlist.replace('[','').replace(']','').split('",')]


## Convert item's property from mongo format to cassandra query format
def stringify(value):
	if isinstance(value, datetime.datetime):
		return '\'' + value.strftime(TIMESTAMP_PATTERN) + '\''
	elif isinstance(value, list):
		return '\'' + str([stringify(item) for item in value]).replace('\'','') + '\''
	elif isinstance(value, dict):
		return ('\"{' + ', '.join([key + ': ' + stringify(value[key]) for key in value]) + '}\"')
	elif isinstance(value, int) or isinstance(value, float):
		return str(value)
	elif isinstance(value, ObjectId):
		return '0x' + str(value)
	elif isinstance(value, bytearray) or isinstance(value, bytes):
		return '0x' + value.hex()
	return '\'' + str(value) + '\''


## Convert item from mongo format to cassandra query format
def querify(item, mode = 'INSERT', keys = None):
	querified = []
	for key in item:
		if (item[key] or (isfloat(item[key]) and item[key] == 0)) and (not isfloat(item[key]) or not math.isnan(item[key])) and (not keys or key in keys):
			try:
				if key.index('__') == 0:
					querified.append([key[2:], stringify(item[key])])
				else:
					querified.append([key, cassandra_stringify_value(item[key])])
			except:
				try:
					if key.index('_') == 0:
						querified.append([key[1:], stringify(item[key])])
					else:
						querified.append([key, cassandra_stringify_value(item[key])])
				except:
					querified.append([key, stringify(item[key])])
					continue

	if mode == 'INSERT':
		return '(' + ', '.join([item[0] for item in querified]) + ') values (' + ', '.join([item[1] for item in querified]) + ')'
	elif mode == 'SELECT':
		criterias = [item[0] + ' = ' + item[1] for item in querified]
		joined_criterias = ' and '.join(criterias)
		return 'where {0} allow filtering'.format(joined_criterias) if (len(criterias) > 0) else joined_criterias
	elif mode == 'DELETE':
		return ' and '.join([item[0] + ' = ' + item[1] for item in querified])


## Convert item, came from cassandra, to mongo format
def repair(item):
	repaired = {}
	for key in item:
		if key == 'cause__':
			continue
		elif key == 'gaps__':
			repaired['__' + key] = string_to_list(item[key])
		elif key == 'workers' or key == 'requirements' or key == 'executors' or key == 'content':
			repaired[key] = string_to_list(item[key])
		else:
			try:
				if key.index('__') == len(key) - 2:
					repaired['__' + key] = item[key]
			except:
				if key == 'id':
					repaired['_' + key] = ObjectId(item[key])
				else:
					#print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,',key)
					if key in ['location', 'state', 'supervisor', 'type', 'department', 'specialization', 'director', 'chief', 'head', 
								'shift', 'operation', 'user', 'system', 'source', 'boat']:
						repaired[key] = ObjectId(item[key])
					else:
						repaired[key] = item[key]

	#print('lllllllllllllllllllllllllllllllllllllll',repaired)

	repaired['__accessed__'] += datetime.timedelta(hours=3)

	return repaired