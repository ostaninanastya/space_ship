import sys, os, datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator
from data_adapters import parse_bytes_parameter, parse_date_parameter, parse_time_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

from system_mapper import SystemMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class SystemTestMapper(graphene.ObjectType):
    
    date = graphene.String()
    time = graphene.String()
    
    system = graphene.Field(lambda: SystemMapper)
    systemid = graphene.String()
    result = graphene.Int()

    def resolve_system(self, info):
        return SystemMapper.init_scalar(mongo_mediator.get_system_by_id(self.system))

    @staticmethod
    def eject(date, time, system, result):
        return [SystemTestMapper.init_scalar(item) for item in cassandra_mediator.select_system_tests(
            date = parse_date_parameter(date),
            time = parse_time_parameter(time),
            system_id = parse_bytes_parameter(system),
            result = result)]

    @staticmethod
    def init_scalar(item):
        return SystemTestMapper(date = date_to_str(item['date']),
                                time = time_to_str(item['time']),
                                system = item['system_id'].hex(),
                                result = item['result'],
                                systemid = item['system_id'].hex())