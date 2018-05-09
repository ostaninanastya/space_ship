import datetime
from bson.objectid import ObjectId

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

def string_to_requirement_entry(strset):
	fields = [item.lstrip().rstrip() for item in strset.replace('{','').replace('}','').replace('"','').split(',')]
	specialization = ObjectId(fields[0].split(':')[1].lstrip().rstrip().replace('id',''))
	quantity = int(fields[1].split(':')[1].lstrip().rstrip())
	return {'specialization': specialization, 'quantity': quantity}

stra = stringify([{'specialization': ObjectId('aaaaaaaaaaaaaaaaaaaaaaac'), 'quantity': 100},{'specialization': ObjectId('aaaaaaaaaaaaaaaaaaaaaaac'), 'quantity': 100}])
#print(stra)
print([string_to_requirement_entry(stra.lstrip().rstrip()) for item in stra.replace('[','').replace(']','').split('",')])