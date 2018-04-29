import sys

import rear_transporter
import intermediate_transporter
import frontal_transporter

fetching_methods = {
	'store': rear_transporter.get_content_on_lower,
	'fast-store': intermediate_transporter.get_content_on_lower,
	'cache': intermediate_transporter.get_content_on_lower
}

def main():
	try:
		return fetching_methods[sys.argv[1]]()
	except Exception as e:
		return 'invalid layer name'

if __name__ == '__main__':
	print(main())