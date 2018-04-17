import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from sensor_mapper import SensorMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

from bson.objectid import ObjectId

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

class UpdateSensors(graphene.Mutation):
    class Arguments:
        name = graphene.String(default_value = '')
        location = graphene.String(default_value = '')
        id = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_location = graphene.String(default_value = '')

    ok = graphene.Boolean()
    sensors = graphene.List(lambda: SensorMapper)

    def mutate(self, info, name, location, set_name, set_location, id):
        sensors = [SensorMapper.init_scalar(item) for item in \
        mongo_native.update_sensor(_id = ObjectId(id) if id else None, name = name, location = ObjectId(location) if location else None, 
            set_name = set_name, set_location = ObjectId(set_location) if set_location else None)]
        ok = True
        return UpdateSensors(sensors = sensors, ok = ok)