import sys, os
from bson.objectid import ObjectId
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from sensor_mapper import SensorMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

from bson.objectid import ObjectId

class CreateSensor(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        location = graphene.String()

    ok = graphene.Boolean()
    sensor = graphene.Field(lambda: SensorMapper)

    def mutate(self, info, name, location):
        sensor = None
        try:
        	sensor = SensorMapper.init_scalar(mongo_mediator.create_sensor(name, location))
        	ok = True
        except IndexError:
        	ok = False
        return CreateSensor(sensor = sensor, ok = ok)

class RemoveSensor(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    sensor = graphene.Field(lambda: SensorMapper)

    def mutate(self, info, id):
        sensor = SensorMapper.init_scalar(mongo_mediator.remove_sensor(id))
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
        sensors = None
        try:
            sensors = [SensorMapper.init_scalar(item) for item in \
            mongo_mediator.update_sensor(_id = ObjectId(id) if id else None, name = name, location = ObjectId(location) if location else None, 
                set_name = set_name, set_location = ObjectId(set_location) if set_location else None)]
            ok = True
        except IndexError:
            ok = False
        return UpdateSensors(sensors = sensors, ok = ok)