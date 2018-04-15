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