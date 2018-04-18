import sys, os
import graphene

from sensor_mapper import SensorMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class SensorDataMapper(graphene.ObjectType):

    date = graphene.String()
    time = graphene.String()

    sourceid = graphene.String()
    source = graphene.Field(SensorMapper)
    event = graphene.String()
    valuename = graphene.String()
    value = graphene.Float()
    units = graphene.String()

    def resolve_source(self, info):
        return SensorMapper.init_scalar(mongo_native.get_sensor_by_id(self.sourceid))

    @staticmethod
    def init_scalar(item):
        return SensorDataMapper(date = date_to_str(item['date']),\
                                 time = time_to_str(item['time']),\
                                 sourceid = item['source_id'].hex(),\
                                 event = item['event'],\
                                 valuename = item['value_name'],\
                                 value = item['value'],\
                                 units = item['units'])