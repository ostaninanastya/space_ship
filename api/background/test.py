import sys, os
import configparser
import datetime
import json

config = configparser.ConfigParser()
config.read('../../databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host']
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

import graphene
from cassandra.cqlengine import connection

sys.path.append('../../logbook/entities')

from position import Position
from control_action import ControlAction

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter
import neo4j_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/native/')

import select_queries

from converters import time_to_str, date_to_str

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from control_action_mapper import ControlActionMapper
from position_mapper import PositionMapper
from system_test_mapper import SystemTestMapper
from operation_state_mapper import OperationStateMapper
from shift_state_mapper import ShiftStateMapper
from sensor_data_mapper import SensorDataMapper

def has_item_valid_time(hour, minute, second, item_time):
    return (hour < 0 or item_time.hour == hour) and\
        (minute < 0 or item_time.minute == minute) and\
        (second < 0 or item_time.second == second)

class FirstQuery(graphene.ObjectType):

    position = graphene.List(PositionMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    controlaction = graphene.List(ControlActionMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    systemtest = graphene.List(SystemTestMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    operationstate = graphene.List(OperationStateMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    shiftstate = graphene.List(ShiftStateMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    sensordata = graphene.List(SensorDataMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))

    def resolve_systemtest(self, info, hour, minute, second):
        return [SystemTestMapper(date = date_to_str(item['date']),\
                                 time = time_to_str(item['time']),\
                                 system = mongo_adapter.get_name_by_id('system_test', item['system_id'].hex()),\
                                 result = item['result'],
                                 systemid = item['system_id'].hex())\
                for item in select_queries.get_system_tests() if \
                                has_item_valid_time(hour, minute, second, item['time'])\
        ]

    def resolve_controlaction(self, info, hour, minute, second):
        return [ControlActionMapper(date = date_to_str(item.date), 
                                    time = time_to_str(item.time),\
                                    macaddress = item.mac_address.hex(),\
                                    username = mongo_adapter.get_name_by_id('user_test', item.user_id.hex()),\
                                    command = item.command,\
                                    params = item.params,\
                                    result = item.result,\
                                    userid = item.user_id.hex())\
                for item in ControlAction.objects.all()[1:] if\
                                has_item_valid_time(hour, minute, second, item.time)\
        ]

    def resolve_position(self, info, hour, minute, second):
        return [PositionMapper(date = date_to_str(item.date),\
                               time = time_to_str(item.time),\
                               x = item.x,\
                               y = item.y,\
                               z = item.z,\
                               speed = item.speed,\
                               attackangle = item.attack_angle,\
                               directionangle = item.direction_angle)\
                for item in Position.objects.all()[1:] if\
                                has_item_valid_time(hour, minute, second, item.time)\
        ]

    def resolve_operationstate(self, info, hour, minute, second):

        return [OperationStateMapper(date = date_to_str(item['date']),\
                               time = time_to_str(item['time']),\
                               boatid = item['boat_id'].hex(),\
                               boatname = mongo_adapter.get_name_by_id('boat_test', item['boat_id'].hex()),\
                               operationid = item['operation_id'].hex(),\
                               #operationname = neo4j_adapter.get_name_by_id('Operation', item['operation_id'].hex()),\
                               #directorid = neo4j_adapter.get_operation_director_id(item['operation_id'].hex()),\
                               #directorname = mongo_adapter.get_name_by_id('people_test', neo4j_adapter.get_operation_director_id(item['operation_id'].hex())),\
                               operationstatus = item['operation_status'],\
                               distancetotheship = item['distance_to_the_ship'],\
                               zenith = item['zenith'],\
                               azimuth = item['azimuth'],\
                               comment = item['comment'])\
                for item in select_queries.get_operation_states() if\
                                has_item_valid_time(hour, minute, second, item['time'])\
        ]

    def resolve_shiftstate(self, info, hour, minute, second):

        return [ShiftStateMapper(date = date_to_str(item['date']),\
                                 time = time_to_str(item['time']),\
                                 shiftid = item['shift_id'].hex(),\
                                 warninglevel = item['warning_level'],\
                                 remainingcartridges = item['remaining_cartridges'],\
                                 remainingelectricity = item['remaining_electricity'],\
                                 remainingair = item['remaining_air'],\
                                 comment = item['comment'])\
                for item in select_queries.get_shift_states() if\
                                has_item_valid_time(hour, minute, second, item['time'])\
        ]

    def resolve_sensordata(self, info, hour, minute, second):

        return [SensorDataMapper(date = date_to_str(item['date']),\
                                 time = time_to_str(item['time']),\
                                 sourceid = item['source_id'].hex(),\
                                 event = item['event'],\
                                 valuename = item['value_name'],\
                                 value = item['value'],\
                                 units = item['units'])\
                for item in select_queries.get_sensor_data() if\
                                has_item_valid_time(hour, minute, second, item['time'])\
        ]

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print('There is no query')
        sys.exit()
    
    connection.setup([DB_URL], DB_NAME)
    schema = graphene.Schema(query = FirstQuery)
    query = sys.argv[1] 
    '''
        query MyFirstQuery {
          position(hour : 20, second : 12){
            x,
            y,
            speed,
            time,
            date
          }
        }
    '''
    print(json.dumps(schema.execute(query).data, indent = 4, sort_keys = True))
    print('=====')