import sys, os, datetime

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator
from data_adapters import parse_bytes_parameter, parse_date_parameter, parse_time_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

class PositionMapper(graphene.ObjectType):
    
    date = graphene.String()
    time = graphene.String()

    x = graphene.Float()
    y = graphene.Float()
    z = graphene.Float()
    speed = graphene.Float()
    attackangle = graphene.Float()
    directionangle = graphene.Float()

    @staticmethod
    def eject(date, time, x, y, z, speed, attack_angle, direction_angle):
      return [PositionMapper.init_scalar(item) for item in cassandra_mediator.select_positions(
            date = parse_date_parameter(date),
            time = parse_time_parameter(time),
            x = x, y = y, z = z, speed = speed, attack_angle = attack_angle, direction_angle = direction_angle)]

    @staticmethod
    def init_scalar(item):
    	return PositionMapper(date = date_to_str(item.date),
                       time = time_to_str(item.time),
                       x = item.x,
                       y = item.y,
                       z = item.z,
                       speed = item.speed,
                       attackangle = item.attack_angle,
                       directionangle = item.direction_angle)