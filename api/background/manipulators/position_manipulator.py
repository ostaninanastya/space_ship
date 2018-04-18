import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from position_mapper import PositionMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

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
        position = PositionMapper.init_scalar(cassandra_mediator.create_position(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN),\
            x, y, z, speed, attackangle, directionangle))
        ok = True
        return CreatePosition(position = position, ok = ok)

class RemovePosition(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()

    ok = graphene.Boolean()
    position = graphene.Field(lambda: PositionMapper)

    def mutate(self, info, timestamp):
        position = PositionMapper.init_scalar(cassandra_mediator.remove_position(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)))
        ok = True
        return RemovePosition(position = position, ok = ok)

class UpdatePositions(graphene.Mutation):
    class Arguments:
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

    def mutate(self, info, timestamp, x, y, z, speed, attackangle, directionangle, set_x, set_y, set_z, set_speed, set_attackangle, set_directionangle):
        parsed_timestamp = None if not timestamp else datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)
        cassandra_mediator.update_positions(date = None if not parsed_timestamp else parsed_timestamp.date,\
            time = None if not parsed_timestamp else parsed_timestamp.time, x = x, y = y, z = z, speed = speed,\
            attackangle = attackangle, directionangle = directionangle, set_x = set_x, set_y = set_y, set_speed = set_speed,\
            set_attackangle = set_attackangle, set_directionangle = set_directionangle)
        ok = True
        return UpdatePositions(ok = ok)