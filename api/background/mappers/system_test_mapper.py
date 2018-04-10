import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

from system_mapper import SystemMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class SystemTestMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()
    
    system = graphene.Field(SystemMapper)
    systemid = graphene.String()
    result = graphene.Int()

    def resolve_system(self, info):
        return SystemMapper.init_scalar(mongo_native.get_system_by_id(self.system))

    @staticmethod
    def init_scalar(item):
        return SystemTestMapper(date = date_to_str(item['date']),
                                time = time_to_str(item['time']),
                                system = item['system_id'].hex(),#mongo_adapter.get_name_by_id('system_test', item['system_id'].hex()),
                                result = item['result'],
                                systemid = item['system_id'].hex())