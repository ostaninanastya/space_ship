import json
from pprint import pprint

renaming = {'hrefToVkCommunity' : 'vk', 'phoneNumber' : 'phone', 'dateOfAdmission' : 'admission', 'comissioningDate' : 'comissioning',
	'serialNumber' : 'serial_number', 'dateOfLaunch' : 'launched', 'dateOfLastChecking' : 'checked', 'personInCharge' : 'supervisor'}

def try_to_repair(key, value, ids):
	if key in ids:
		return {'$oid' : int(value).to_bytes(12, byteorder='big').hex()}
	try:
		return float(value)
	except:
		return value

def validate_key(key):
	if key in renaming:
		return renaming[key]
	return key

def convert(filepath, base, ids = []):
	data = json.load(open(filepath))
	new_filename = ''.join(filepath.split('.')[:-1]) + '-mongo.json'
	with open(new_filename, 'w') as outfile:
		outfile.write('')
	with open(new_filename, 'a') as outfile:
		for item in data[base]:
			json.dump(dict({ validate_key(key) : try_to_repair(key, item[key], ids) for key in item if key != 'id'}, **{'_id' : {'$oid' : int(item['id']).to_bytes(12, byteorder='big').hex()}}), outfile)
	return new_filename

if __name__ == '__main__':
	convert('boats.json', 'boats')