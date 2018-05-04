import unittest
import crud_test
from crud_test import TestCrud

crud_test.SINGULAR = 'system'
crud_test.PLURAL = 'systems'

crud_test.FIELDS_TO_SHOW = 'name,id'
crud_test.CHECKING_PARAM = 'name'

crud_test.FIRST_VALUE = 'Pomegranate'
crud_test.SECOND_VALUE = 'Avocado'

crud_test.CREATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.FIRST_VALUE + '\'', 
	'launched': "'2012-12-12%2013:59:12'", 'checked': "'2013-12-12%2013:59:12'", 'serialnumber': 0.11, 
	'state': "'000000000000000000000003'", 'type': "'000000000000000000000002'", 'supervisor': "'000000000000000000000002'"}
crud_test.UPDATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.SECOND_VALUE + '\''}

if __name__ == '__main__':
    unittest.main()