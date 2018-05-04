import unittest
import crud_test
from crud_test import TestCrud

crud_test.SINGULAR = 'person'
crud_test.PLURAL = 'people'

crud_test.FIELDS_TO_SHOW = 'name,id'
crud_test.CHECKING_PARAM = 'name'

crud_test.FIRST_VALUE = 'Pomegranate'
crud_test.SECOND_VALUE = 'Avocado'

crud_test.CREATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.FIRST_VALUE + '\'', 
	'surname': "'Ivanov'", 'phone': "'8%20911%20111-11-11'", 'department': "'000000000000000000000001'", 'specialization': "'000000000000000000000001'"}
crud_test.UPDATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.SECOND_VALUE + '\''}

if __name__ == '__main__':
    unittest.main()