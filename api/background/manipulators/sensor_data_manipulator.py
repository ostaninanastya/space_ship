import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from sensor_data_mapper import SensorDataMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator
from data_adapters import string_to_bytes

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

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
        sensor_data = SensorDataMapper.init_scalar(cassandra_mediator.create_sensor_data(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN),\
            source, event, meaning, value, units))
        ok = True
        return CreateSensorData(sensor_data = sensor_data, ok = ok)

class RemoveSensorData(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()

    ok = graphene.Boolean()
    sensor_data = graphene.Field(lambda: SensorDataMapper)

    def mutate(self, info, timestamp):
        sensor_data = SensorDataMapper.init_scalar(cassandra_mediator.remove_sensor_data(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)))
        ok = True
        return RemoveSensorData(sensor_data = sensor_data, ok = ok)

class UpdateSensorData(graphene.Mutation):
    class Arguments:
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

    ok = graphene.Boolean()

    def mutate(self, info, timestamp, source, event, meaning, value, units, set_source, set_event, set_meaning, set_value, set_units):
        parsed_timestamp = None if not timestamp else datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)
        cassandra_mediator.update_sensor_data(date = None if not parsed_timestamp else parsed_timestamp.date(),\
            time = None if not parsed_timestamp else parsed_timestamp.time(),
            source_id = source, event = event, meaning = meaning, value = value, units = units,
            set_source_id = None if not set_source else SensorData.validate_source_id(string_to_bytes(set_source)),
            set_event = None if not set_event else SensorData.validate_event(set_event), 
            set_value_name = None if not set_meaning else SensorData.validate_value_name(set_value_name),
            set_value = set_value, 
            set_units = None if not set_units else SensorData.validate_units(set_units))
        ok = True
        return UpdateSensorData(ok = ok)