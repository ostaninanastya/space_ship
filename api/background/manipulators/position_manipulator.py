import sys, os
import configparser
import datetime
import graphene
from bson.objectid import ObjectId

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from position_mapper import PositionMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import string_to_bytes, parse_timestamp_parameter, parse_objectid_parameter, parse_bytes_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class CreatePosition(graphene.Mutation):
    class Arguments:

        timestamp = graphene.String()
        x = graphene.Float()
        y = graphene.Float()
        z = graphene.Float()
        speed = graphene.Float()
        attackangle = graphene.Float()
        directionangle = graphene.Float()

    ok = graphene.Boolean()
    position = graphene.Field(lambda: PositionMapper)

    def mutate(self, info, timestamp, x, y, z, speed, attackangle, directionangle):
        position = PositionMapper.init_scalar(mongo_mediator.create_position(parse_timestamp_parameter(timestamp), x, y, z, speed, attackangle, directionangle))
        ok = True
        return CreatePosition(position = position, ok = ok)

class RemovePosition(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    position = graphene.Field(lambda: PositionMapper)

    def mutate(self, info, id):
        position = PositionMapper.init_scalar(mongo_mediator.remove_position(id))
        ok = True
        return RemovePosition(position = position, ok = ok)

class UpdatePositions(graphene.Mutation):
    class Arguments:

        id = graphene.String(default_value = '')
        timestamp = graphene.String(default_value = '')
        x = graphene.Float(default_value = float('nan'))
        y = graphene.Float(default_value = float('nan'))
        z = graphene.Float(default_value = float('nan'))
        speed = graphene.Float(default_value = float('nan'))
        attackangle = graphene.Float(default_value = float('nan'))
        directionangle = graphene.Float(default_value = float('nan'))

        set_x = graphene.Float(default_value = float('nan'))
        set_y = graphene.Float(default_value = float('nan'))
        set_z = graphene.Float(default_value = float('nan'))
        set_speed = graphene.Float(default_value = float('nan'))
        set_attackangle = graphene.Float(default_value = float('nan'))
        set_directionangle = graphene.Float(default_value = float('nan'))

    ok = graphene.Boolean()

    def mutate(self, info, id, timestamp, x, y, z, speed, attackangle, directionangle, set_x, set_y, set_z, set_speed, set_attackangle, set_directionangle):
        cassandra_mediator.update_positions(id = parse_objectid_parameter(id), timestamp = parse_timestamp_parameter(timestamp),
            x = x, y = y, z = z, speed = speed, attack_angle = attackangle, direction_angle = direction_angle, 
            set_x = set_x, set_y = set_y, set_z = set_z, set_speed = set_speed, set_attack_angle = set_attackangle, 
            set_direction_angle = set_directionangle)
        ok = True
        return UpdatePositions(ok = ok)