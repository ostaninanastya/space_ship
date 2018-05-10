import sys, os
import configparser
import datetime
import graphene
from bson.objectid import ObjectId

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from sensor_data_mapper import SensorDataMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import string_to_bytes, parse_timestamp_parameter, parse_objectid_parameter, parse_bytes_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class CreateSensorData(graphene.Mutation):
    class Arguments:

        timestamp = graphene.String()
        source = graphene.String()
        event = graphene.String()
        meaning = graphene.String()
        value = graphene.Float()
        units = graphene.String()

    ok = graphene.Boolean()
    sensor_data = graphene.Field(lambda: SensorDataMapper)

    def mutate(self, info, timestamp, source, event, meaning, value, units):
        sensor_data = None
        try:
            sensor_data = SensorDataMapper.init_scalar(mongo_mediator.create_sensor_data(parse_timestamp_parameter(timestamp),
                parse_objectid_parameter(source), event, meaning, value, units))
            ok = True
        except IndexError:
            ok = False
        return CreateSensorData(sensor_data = sensor_data, ok = ok)

class RemoveSensorData(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    sensor_data = graphene.Field(lambda: SensorDataMapper)

    def mutate(self, info, id):
        sensor_data = SensorDataMapper.init_scalar(mongo_mediator.remove_sensor_data(id))
        ok = True
        return RemoveSensorData(sensor_data = sensor_data, ok = ok)

class UpdateSensorData(graphene.Mutation):
    class Arguments:

        id = graphene.String(default_value = '')
        timestamp = graphene.String(default_value = '')
        source = graphene.String(default_value = '')
        event = graphene.String(default_value = '')
        meaning = graphene.String(default_value = '')
        value = graphene.Float(default_value = float('nan'))
        units = graphene.String(default_value = '')

        set_source = graphene.String(default_value = '')
        set_event = graphene.String(default_value = '')
        set_meaning = graphene.String(default_value = '')
        set_value = graphene.Float(default_value = float('nan'))
        set_units = graphene.String(default_value = '')
        set_timestamp = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, id, timestamp, source, event, meaning, value, units, set_source, set_event, set_meaning, set_value, set_units, set_timestamp):
        try:
            mongo_mediator.update_sensor_data(_id = parse_objectid_parameter(id), timestamp = parse_timestamp_parameter(timestamp),
                source = parse_objectid_parameter(source), event = event, meaning = meaning, value = value, units = units,
                set_source = parse_objectid_parameter(set_source), set_event = set_event, 
                set_meaning = set_meaning, set_value = set_value, set_units = set_units, set_timestamp = parse_timestamp_parameter(set_timestamp))
            ok = True
        except IndexError:
            ok = False
        return UpdateSensorData(ok = ok)