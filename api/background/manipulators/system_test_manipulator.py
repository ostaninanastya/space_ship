import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from system_test_mapper import SystemTestMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/entities')

from system_test import SystemTest

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator
from data_adapters import string_to_bytes

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

class UpdateSystemTests(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String(default_value = '')
        system = graphene.String(default_value = '')
        result = graphene.Int(default_value = -1)

        set_system = graphene.String(default_value = '')
        set_result = graphene.Int(default_value = -1)

    ok = graphene.Boolean()

    def mutate(self, info, timestamp, system, result, set_system, set_result):
        parsed_timestamp = None if not timestamp else datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)
        SystemTest.validate_system_id(string_to_bytes(set_system))
        cassandra_mediator.update_system_tests(date = None if not parsed_timestamp else parsed_timestamp.date,\
            time = None if not parsed_timestamp else parsed_timestamp.time, system_id = None if not system else string_to_bytes(system),\
            result = result, set_system_id = None if not set_system else string_to_bytes(set_system), set_result = set_result)
        ok = True
        return UpdateSystemTests(ok = ok)