import unittest
import crud_test_cassandra as crud_test
from crud_test_cassandra import TestCrud

crud_test.SINGULAR = 'position'
crud_test.PLURAL = 'positions'


crud_test.FIELDS_TO_SHOW = 'date,time,x,y,z'
crud_test.CHECKING_PARAM = 'z'

crud_test.FIRST_VALUE = 666.666
crud_test.SECOND_VALUE = 333.333

crud_test.CREATE_PARAMS = {'timestamp': "'2112-12-11 12:12:12'", 'x': 1.0, 'y': 1.0, crud_test.CHECKING_PARAM: crud_test.FIRST_VALUE, 
	'speed': 1.0, 'attackangle': 1.0, 'directionangle': 1.0}
crud_test.UPDATE_PARAMS = {crud_test.CHECKING_PARAM: crud_test.SECOND_VALUE}

#http://localhost:1881/api/create/position/fields=ok,position(x)&where=timestamp:'2017-02-18%2023:59:57',x:10.0,y:10.2,z:10.3,speed:10.4,attackangle:10.5,directionangle:10.6
#http://localhost:1881/api/create/position/fields=position(timestamp,x,y,z)&where=timestamp:'2111-11-11%2012:12:12',x:1.0,y:1.0,z:1.0,speed:1.0,attackangle:1.0,directionangle:1.0


if __name__ == '__main__':
    unittest.main()