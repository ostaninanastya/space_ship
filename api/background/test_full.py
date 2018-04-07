import sys, os
import configparser
import datetime

config = configparser.ConfigParser()
config.read('../../databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host']
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

import graphene
from cassandra.cqlengine import connection

sys.path.append('../../logbook/entities')

from position import Position

class Simplest(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    surname = graphene.String()

simplests = [
    Simplest(name='oko', surname='ivanov'),
    Simplest(name='baka', surname='ivanov'),
    Simplest(name='foo', surname='sydorov')
]


class Query(graphene.ObjectType):

    position = graphene.String(id = graphene.String())

    def resolve_position(self, info, id):
        return 'ok'

class SimplestQuery(graphene.ObjectType):

    human = graphene.List(Simplest,
                           surname=graphene.String()
                           )


    def resolve_human(self, info, surname):
        global simplests
        print(id)
        return [item for item in simplests if item.surname == surname]

class PositionMapper(graphene.ObjectType):
    x = graphene.Float()
    y = graphene.Float()
    z = graphene.Float()

    speed = graphene.Float()
    attack_angle = graphene.Float()
    direction_angle = graphene.Float()

def time_to_str(t):
    return str(t.hour) + ':' + ('%02d' % t.minute) + ':' + ('%02d' % t.second)


class FirstQuery(graphene.ObjectType):

    position = graphene.List(PositionMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))


    def resolve_position(self, info, hour, minute, second):
        #print(date)
        print([time_to_str(item.time) for item in Position.objects.all()[1:]])
        return [PositionMapper(x = item.x, y = item.y, z = item.z, speed = item.speed, attack_angle = item.attack_angle, direction_angle = item.direction_angle)\
            for item in Position.objects.all()[1:] if\
            (hour < 0 or item.time.hour == hour) and\
            (minute < 0 or item.time.minute == minute) and\
            (second < 0 or item.time.second == second)\
        ]


'''
class Query(graphene.ObjectType):
    hello = graphene.String(name = graphene.String(default_value = "stranger"))

    def resolve_hello(self, info, name):
        print('ok')
        return ['Hello ' + name, 'okoe']
'''

if __name__ == '__main__':
    connection.setup([DB_URL], DB_NAME)
    schema = graphene.Schema(query = FirstQuery)
    query = '''
        query Zalupa {
          position(hour : 20, second : 12){
            x,
            y,
            speed
          }
        }
    '''
    print(schema.execute(query).data)

    '''
    connection.setup([DB_URL], DB_NAME)
	
    schema = graphene.Schema(query=Query)

    query = 
        query PositionQuery {
          position(id: "1000") {
            time
          }
        }
    

    result = schema.execute(query)
    print(result.data)
    '''