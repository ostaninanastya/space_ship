import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from system_test_mapper import SystemTestMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateSystemTest(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()
        system = graphene.String()
        result = graphene.Int()

    ok = graphene.Boolean()
    systemtest = graphene.Field(lambda: SystemTestMapper)

    def mutate(self, info, timestamp, system, result):
        systemtest = SystemTestMapper.init_scalar(cassandra_mediator.create_system_test(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN),\
            system, result))
        ok = True
        return CreateSystemTest(systemtest = systemtest, ok = ok)

class RemoveSystemTest(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()

    ok = graphene.Boolean()
    systemtest = graphene.Field(lambda: SystemTestMapper)

    def mutate(self, info, timestamp):
        systemtest = SystemTestMapper.init_scalar(cassandra_mediator.remove_system_test(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)))
        ok = True
        return RemoveSystemTest(systemtest = systemtest, ok = ok)