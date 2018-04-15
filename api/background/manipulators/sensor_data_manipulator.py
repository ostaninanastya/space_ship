import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from sensor_data_mapper import SensorDataMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator

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
    sensordata = graphene.Field(lambda: SensorDataMapper)

    def mutate(self, info, timestamp, source, event, meaning, value, units):
        sensordata = SensorDataMapper.init_scalar(cassandra_mediator.create_sensor_data(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN),\
            source, event, meaning, value, units))
        ok = True
        return CreateSensorData(sensordata = sensordata, ok = ok)

class RemoveSensorData(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()

    ok = graphene.Boolean()
    sensordata = graphene.Field(lambda: SensorDataMapper)

    def mutate(self, info, timestamp):
        sensordata = SensorDataMapper.init_scalar(cassandra_mediator.remove_sensor_data(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)))
        ok = True
        return RemoveSensorData(sensordata = sensordata, ok = ok)