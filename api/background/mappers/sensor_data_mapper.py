import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import parse_bytes_parameter, parse_timestamp_parameter, stringify_timestamp_parameter, parse_objectid_parameter

from sensor_mapper import SensorMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class SensorDataMapper(graphene.ObjectType):

    id = graphene.String()
    timestamp = graphene.String()

    source = graphene.Field(lambda: SensorMapper)
    event = graphene.String()
    valuename = graphene.String()
    value = graphene.Float()
    units = graphene.String()

    def resolve_source(self, info):
        return SensorMapper.init_scalar(mongo_mediator.get_sensor_by_id(self.source))

    @staticmethod
    def eject(id, timestamp, sensor, event, valuename, value, units):
        return [SensorDataMapper.init_scalar(item) for item in mongo_mediator.select_sensor_data(timestamp = parse_timestamp_parameter(timestamp),
            source = parse_objectid_parameter(sensor), event = event, value_name = valuename, value = value, units = units, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        return SensorDataMapper(id = str(item['_id']),
                                 timestamp = stringify_timestamp_parameter(item['timestamp']),
                                 source = str(item['source']),
                                 event = item['event'],
                                 valuename = item['meaning'],
                                 value = item['value'],
                                 units = item['units'])