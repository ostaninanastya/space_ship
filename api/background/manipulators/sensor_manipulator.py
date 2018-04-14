import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from sensor_mapper import SensorMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class CreateSensor(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        location = graphene.String()

    ok = graphene.Boolean()
    sensor = graphene.Field(lambda: SensorMapper)

    def mutate(self, info, name, location):
        print('omg')
        sensor = SensorMapper.init_scalar(mongo_native.create_sensor(name, location))
        ok = True
        return CreateSensor(sensor = sensor, ok = ok)

class RemoveSensor(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    sensor = graphene.Field(lambda: SensorMapper)

    def mutate(self, info, id):
        sensor = SensorMapper.init_scalar(mongo_native.remove_sensor(id))
        ok = True
        return RemoveSensor(sensor = sensor, ok = ok)