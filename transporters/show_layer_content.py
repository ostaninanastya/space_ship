import sys
import json

import rear_transporter
import intermediate_transporter
import frontal_transporter

fetching_methods = {
	'store': rear_transporter.get_content_on_lower,
	'fast-store': intermediate_transporter.get_content_on_lower,
	'cache': intermediate_transporter.get_content_on_lower
}

def show_pretty(dicti, padding = 0):
	result = ''
	if isinstance(dicti, dict):
		result += '{\n'
		for key in dicti:
			result += '{0}{1}: {2};\n'.format(' '*(padding + 4), key, show_pretty(dicti[key], padding + 8))
		result += '{0}}}'.format(' '*padding)
		return result
	elif isinstance(dicti, list):
		result += '[\n'
		for item in dicti:
			result += '{0}{1},\n'.format(' '*(padding + 4), show_pretty(item, padding + 4))
		result += '{0}]'.format(' '*padding)
		return result
	else:
		return(str(dicti))

def main():
	#try:
	return fetching_methods[sys.argv[1]]()
	#except Exception as e:
	#	print(e)
	#	return 'invalid layer name'

if __name__ == '__main__':
	#print(main())
	print(show_pretty(main(), padding = 0))
	#print 