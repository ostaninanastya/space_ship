import json
from pprint import pprint

renaming = {'system' : 'system_id', 'sensor_id' : 'source_id'}

def try_to_repair(key, value, mongo_ids, neo_ids, strings):
	if key in mongo_ids:
		return "0x" + int(value).to_bytes(12, byteorder='big').hex()
	if key in neo_ids:
		return "0x" + int(value).to_bytes(16, byteorder='big').hex()
	if key == "time" and len(value) == 5:
		return value + ":00"
	if key == "mac_address":
		return "0x" + abs(int(value)).to_bytes(6, byteorder='big').hex()
	if key in strings:
		return value
	try:
		floated = float(value)
		if floated - int(floated) == 0:
			return int(floated)
		return floated
	except:
		return value

def validate_key(key):
	if key in renaming:
		return renaming[key]
	return key

def convert(filepath, base, mongo_ids = [], neo_ids = [], strings = []):
	data = json.load(open(filepath))
	new_filename = ''.join(filepath.split('.')[:-1]) + '-cassandra.json'

	result = {"data" : []}

	for item in data[base]:
		result["data"].append({ validate_key(key) : try_to_repair(key, item[key], mongo_ids, neo_ids, strings) for key in item })

	with open(new_filename, 'w') as outfile:
		json.dump(result, outfile)

	return new_filename

if __name__ == '__main__':
	convert('/home/zeionara/Documents/tst.json', 'system_test', mongo_ids = ['system'])