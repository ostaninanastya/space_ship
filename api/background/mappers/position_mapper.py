import sys, os, datetime
from bson.objectid import ObjectId
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import parse_bytes_parameter, parse_timestamp_parameter, stringify_timestamp_parameter, parse_objectid_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class PositionMapper(graphene.ObjectType):
    
    id = graphene.String()
    timestamp = graphene.String()

    x = graphene.Float()
    y = graphene.Float()
    z = graphene.Float()
    speed = graphene.Float()
    attackangle = graphene.Float()
    directionangle = graphene.Float()

    @staticmethod
    def eject(id, timestamp, x, y, z, speed, attack_angle, direction_angle):
      return [PositionMapper.init_scalar(item) for item in mongo_mediator.select_positions(
            timestamp = parse_timestamp_parameter(timestamp),
            x = x, y = y, z = z, speed = speed, attack_angle = attack_angle, direction_angle = direction_angle, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
    	return PositionMapper(
                       id = str(item['_id']),
                       timestamp = stringify_timestamp_parameter(item['timestamp']),
                       x = item['x'],
                       y = item['y'],
                       z = item['z'],
                       speed = item['speed'],
                       attackangle = item['attack_angle'],
                       directionangle = item['direction_angle'])