import unittest
import crud_test_cassandra as crud_test
from crud_test_cassandra import TestCrud

crud_test.SINGULAR = 'operationState'
crud_test.PLURAL = 'operationStates'

crud_test.FIELDS_TO_SHOW = 'date,time,comment'
crud_test.CHECKING_PARAM = 'comment'

crud_test.FIRST_VALUE = 'all is good'
crud_test.SECOND_VALUE = 'all is bad'

crud_test.CREATE_PARAMS = {'timestamp': "'2112-12-11 12:12:12'", 'boat': "'000000000000000000000003'", 'operation': "'00000000000000000000000000000014'", 
	'status': "'returning'", 'distancetotheship': 25.3, 'zenith': 13.1, 'azimuth': 13.1, 'moscovium': 50, 'helium': 50,
	crud_test.CHECKING_PARAM: '\'' + crud_test.FIRST_VALUE + '\''}
crud_test.UPDATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.SECOND_VALUE + '\''}

#http://localhost:1881/api/create/position/fields=ok,position(x)&where=timestamp:'2017-02-18%2023:59:57',x:10.0,y:10.2,z:10.3,speed:10.4,attackangle:10.5,directionangle:10.6
#http://localhost:1881/api/create/position/fields=position(timestamp,x,y,z)&where=timestamp:'2111-11-11%2012:12:12',x:1.0,y:1.0,z:1.0,speed:1.0,attackangle:1.0,directionangle:1.0


if __name__ == '__main__':
    unittest.main()