import unittest
import crud_test_cassandra as crud_test
from crud_test_cassandra import TestCrud

crud_test.SINGULAR = 'shiftState'
crud_test.PLURAL = 'shistStates'

crud_test.FIELDS_TO_SHOW = 'date,time,comment'
crud_test.CHECKING_PARAM = 'comment'

crud_test.FIRST_VALUE = 'all is good'
crud_test.SECOND_VALUE = 'all is bad'

crud_test.CREATE_PARAMS = {'timestamp': "'2112-12-11 12:12:12'", 'shift': "'00000000000000000000000000000014'", 
	'warninglevel': "'low'", 'remainingcartridges': 25, 'remainingair': 25, 'remainingelectricity': 25,
	crud_test.CHECKING_PARAM: '\'' + crud_test.FIRST_VALUE + '\''}
crud_test.UPDATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.SECOND_VALUE + '\''}

#http://localhost:1881/api/create/position/fields=ok,position(x)&where=timestamp:'2017-02-18%2023:59:57',x:10.0,y:10.2,z:10.3,speed:10.4,attackangle:10.5,directionangle:10.6
#http://localhost:1881/api/create/position/fields=position(timestamp,x,y,z)&where=timestamp:'2111-11-11%2012:12:12',x:1.0,y:1.0,z:1.0,speed:1.0,attackangle:1.0,directionangle:1.0


if __name__ == '__main__':
    unittest.main()