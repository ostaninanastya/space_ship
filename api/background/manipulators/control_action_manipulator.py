import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from control_action_mapper import ControlActionMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateControlAction(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()
        mac = graphene.String()
        user = graphene.String()
        command = graphene.String()
        params = graphene.String()
        result = graphene.String()

    ok = graphene.Boolean()
    controlaction = graphene.Field(lambda: ControlActionMapper)

    def mutate(self, info, timestamp, mac, user, command, params, result):
        controlaction = ControlActionMapper.init_scalar(cassandra_mediator.create_control_action(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN),\
            mac, user, command, params, result))
        ok = True
        return CreateControlAction(controlaction = controlaction, ok = ok)

class RemoveControlAction(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()

    ok = graphene.Boolean()
    controlaction = graphene.Field(lambda: ControlActionMapper)

    def mutate(self, info, timestamp):
        controlaction = ControlActionMapper.init_scalar(cassandra_mediator.remove_control_action(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)))
        ok = True
        return RemoveControlAction(controlaction = controlaction, ok = ok)