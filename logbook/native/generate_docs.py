import sys, os

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/')

from data_adapters import get_strings

in_table = False

for item in get_strings('genesis_ilm.sql'):
	if 'create table' in item:
		in_table = True
		print('## ' + item.split('cache.')[1].split(' ')[0])
		print('|property|data type|')
		print('|--------|---------|')
	elif 'PRIMARY' in item:
		in_table = False
	elif in_table:
		field_name, field_type = item.split(' ')
		if '__' in field_name:
			field_name = '__' + field_name
			if field_name == '__gaps__':
				field_type = 'list of numbers'
		elif 'id' in field_name:
			field_name = '_' + field_name
		print(' | ', field_name.replace('_','\\_'), ' | ', field_type.replace(',',''), ' | ')