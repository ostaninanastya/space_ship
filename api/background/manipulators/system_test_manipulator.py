import sys, os
import configparser
import datetime
import graphene
from bson.objectid import ObjectId

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from system_test_mapper import SystemTestMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/entities')

from system_test import SystemTest

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import string_to_bytes, parse_timestamp_parameter, parse_objectid_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator


class CreateSystemTest(graphene.Mutation):
    class Arguments:
        
        timestamp = graphene.String()
        system = graphene.String()
        result = graphene.Int()

    ok = graphene.Boolean()
    system_test = graphene.Field(lambda: SystemTestMapper)

    def mutate(self, info, timestamp, system, result):
        system_test = None
        try:
            system_test = SystemTestMapper.init_scalar(mongo_mediator.create_system_test(parse_timestamp_parameter(timestamp), 
                parse_objectid_parameter(system), result))
            ok = True
        except IndexError:
            ok = False
        return CreateSystemTest(system_test = system_test, ok = ok)

class RemoveSystemTest(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    system_test = graphene.Field(lambda: SystemTestMapper)

    def mutate(self, info, id):
        system_test = SystemTestMapper.init_scalar(mongo_mediator.remove_system_test(id))
        ok = True
        return RemoveSystemTest(system_test = system_test, ok = ok)

class UpdateSystemTests(graphene.Mutation):
    class Arguments:
        
        id = graphene.String(default_value = '')
        timestamp = graphene.String(default_value = '')
        system = graphene.String(default_value = '')
        result = graphene.Int(default_value = -1)

        set_system = graphene.String(default_value = '')
        set_result = graphene.Int(default_value = -1)
        set_timestamp = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, timestamp, system, result, set_system, set_result, id, set_timestamp):
        try:
            mongo_mediator.update_system_tests(_id = parse_objectid_parameter(id), 
                timestamp = parse_timestamp_parameter(timestamp), system = parse_objectid_parameter(system),
                result = result if result > 0 else None, set_system_id = parse_objectid_parameter(set_system), 
                set_result = set_result if set_result > 0 else None, 
                set_timestamp = parse_timestamp_parameter(set_timestamp))
            ok = True
        except IndexError:
            ok = False
        return UpdateSystemTests(ok = ok)