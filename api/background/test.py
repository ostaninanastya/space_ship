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

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/native/')

import select_queries

def time_to_str(t):
    return ('%02d' % t.hour) + ':' + ('%02d' % t.minute) + ':' + ('%02d' % t.second)

def date_to_str(t):
    return str(t)

class SystemTestMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()
    
    system = graphene.String()
    result = graphene.Int()

class PositionMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()

    x = graphene.Float()
    y = graphene.Float()
    z = graphene.Float()

    speed = graphene.Float()
    attackangle = graphene.Float()
    directionangle = graphene.Float()

class ControlActionMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()
    
    macaddress = graphene.String()
    username = graphene.String()
    
    command = graphene.String()
    params = graphene.String()
    result = graphene.String()

class FirstQuery(graphene.ObjectType):

    position = graphene.List(PositionMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    controlaction = graphene.List(ControlActionMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    systemtest = graphene.List(SystemTestMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))

    def resolve_systemtest(self, info, hour, minute, second):
        #print(select_queries.get_system_tests())
        return [SystemTestMapper(date = date_to_str(item['date']), time = time_to_str(item['time']),\
            system = mongo_adapter.get_name_by_id('system_test', item['system_id'].hex()), result = item['result'])\
            for item in select_queries.get_system_tests() if\
            (hour < 0 or item['time'].hour == hour) and\
            (minute < 0 or item['time'].minute == minute) and\
            (second < 0 or item['time'].second == second)\
        ]

    def resolve_controlaction(self, info, hour, minute, second):
        #print([mongo_adapter.get_name_by_id('system_test', item['system_id'].hex()) for item in select_queries.get_system_tests()])
        return [ControlActionMapper(date = date_to_str(item.date), time = time_to_str(item.time),\
            macaddress = item.mac_address, username = mongo_adapter.get_name_by_id('user_test', item.user_id.hex()),\
            command = item.command, params = item.params, result = item.result)\
            for item in ControlAction.objects.all()[1:] if\
            (hour < 0 or item.time.hour == hour) and\
            (minute < 0 or item.time.minute == minute) and\
            (second < 0 or item.time.second == second)\
        ]

    def resolve_position(self, info, hour, minute, second):
        #print([mongo_adapter.get_name_by_id('user_test', item.user_id.hex()) for item in ControlAction.objects.all()])
        return [PositionMapper(date = date_to_str(item.date), time = time_to_str(item.time), x = item.x, y = item.y, z = item.z, speed = item.speed, attackangle = item.attack_angle, directionangle = item.direction_angle)\
            for item in Position.objects.all()[1:] if\
            (hour < 0 or item.time.hour == hour) and\
            (minute < 0 or item.time.minute == minute) and\
            (second < 0 or item.time.second == second)\
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