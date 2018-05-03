import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator
from data_adapters import parse_bytes_parameter, parse_date_parameter, parse_time_parameter

from sensor_mapper import SensorMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class SensorDataMapper(graphene.ObjectType):

    date = graphene.String()
    time = graphene.String()

    source = graphene.Field(lambda: SensorMapper)
    event = graphene.String()
    valuename = graphene.String()
    value = graphene.Float()
    units = graphene.String()

    def resolve_source(self, info):
        return SensorMapper.init_scalar(mongo_mediator.get_sensor_by_id(self.source))

    @staticmethod
    def eject(date, time, sensor, event, valuename, value, units):
        return [SensorDataMapper.init_scalar(item) for item in cassandra_mediator.select_sensor_data(
            date = parse_date_parameter(date), 
            time = parse_time_parameter(time),
            source_id = parse_bytes_parameter(sensor), 
            event = event, value_name = valuename, value = value, units = units)]

    @staticmethod
    def init_scalar(item):
        return SensorDataMapper(date = date_to_str(item['date']),
                                 time = time_to_str(item['time']),
                                 source = item['source_id'].hex(),
                                 event = item['event'],
                                 valuename = item['value_name'],
                                 value = item['value'],
                                 units = item['units'])