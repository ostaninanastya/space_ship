import unittest
import crud_test
from crud_test import TestCrud

crud_test.SINGULAR = 'property'
crud_test.PLURAL = 'properties'

crud_test.FIELDS_TO_SHOW = 'name,id'
crud_test.CHECKING_PARAM = 'name'

crud_test.FIRST_VALUE = 'Pomegranate'
crud_test.SECOND_VALUE = 'Avocado'

crud_test.CREATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.FIRST_VALUE + '\'', 
	'admission': "'2012-12-12%2013:59:12'", 'comissioning': "'2013-12-12%2013:59:12'", 
	'type':"'000000000000000000000001'", 'department': "'000000000000000000000001'"}
crud_test.UPDATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.SECOND_VALUE + '\''}

if __name__ == '__main__':
    unittest.main()