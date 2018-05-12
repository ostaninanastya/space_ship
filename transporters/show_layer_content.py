import sys
import json

import rear_transporter
import intermediate_transporter
import frontal_transporter

fetching_methods = {
	'store': rear_transporter.get_content_on_lower,
	'fast-store': intermediate_transporter.get_content_on_lower,
	'cache': frontal_transporter.get_content_on_lower,
	'hot-cache': frontal_transporter.get_content_on_upper
}

def try_to_repair(value):
	try:
		return float(value)
	except:
		return '"{0}"'.format(value)

def delete_last_comma(string):
	k = string.rfind(",")
	return string[:k] + string[k+1:]

def show_pretty(dicti, padding = 0):
	result = ''
	if isinstance(dicti, dict):
		result += '{\n'
		for key in dicti:
			result += '{0}"{1}": {2},\n'.format(' '*(padding + 4), key, show_pretty(dicti[key], padding + 8))
		result += '{0}}}'.format(' '*padding)
		return delete_last_comma(result)
	elif isinstance(dicti, list):
		result += '[\n'
		index = 0
		for item in dicti:
			index += 1
			result += '{0}{1}{2}\n'.format(' '*(padding + 4), show_pretty(item, padding + 4), ',' if index < len(dicti) else '')
		result += '{0}]'.format(' '*padding)
		return result
	else:
		return try_to_repair(dicti)

def main():
	#try:
	if len(sys.argv) < 3 or not sys.argv[2]:
		return fetching_methods[sys.argv[1]]()
	else:
		return {sys.argv[2]: fetching_methods[sys.argv[1]]()[sys.argv[2]]}
	#except Exception as e:
	#	print(e)
	#	return 'invalid layer name'

if __name__ == '__main__':
	#print(main())
	print(show_pretty(main(), padding = 0))
	print('====')
	#print 