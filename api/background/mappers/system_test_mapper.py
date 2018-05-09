import sys, os, datetime
import graphene
from bson.objectid import ObjectId

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import parse_bytes_parameter, parse_timestamp_parameter, stringify_timestamp_parameter, parse_objectid_parameter

from system_mapper import SystemMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class SystemTestMapper(graphene.ObjectType):
    
    id = graphene.String()
    timestamp = graphene.String()
    system = graphene.Field(lambda: SystemMapper)
    result = graphene.Int()

    def resolve_system(self, info):
        return SystemMapper.init_scalar(mongo_mediator.get_system_by_id(self.system))

    @staticmethod
    def eject(id, timestamp, system, result):
        return [SystemTestMapper.init_scalar(item) for item in mongo_mediator.select_system_tests(
            timestamp = parse_timestamp_parameter(timestamp),
            system = parse_objectid_parameter(system),
            result = result if result != -1 else None, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        print(item)
        return SystemTestMapper(id = str(item['_id']),
                                timestamp = stringify_timestamp_parameter(item['timestamp']),
                                system = str(item['system']),
                                result = item['result'])