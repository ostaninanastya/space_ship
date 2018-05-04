import unittest
import crud_test
from crud_test import TestCrud

crud_test.SINGULAR = 'specialization'
crud_test.PLURAL = 'specializations'

crud_test.FIELDS_TO_SHOW = 'name,id'
crud_test.CHECKING_PARAM = 'name'

crud_test.FIRST_VALUE = 'Pomegranate'
crud_test.SECOND_VALUE = 'Avocado'

crud_test.CREATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.FIRST_VALUE + '\''}
crud_test.UPDATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.SECOND_VALUE + '\''}

if __name__ == '__main__':
    unittest.main()