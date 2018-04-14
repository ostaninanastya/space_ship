import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class LocationMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    sensors = graphene.List('sensor_mapper.SensorMapper')

    def resolve_sensors(self, info):
        from sensor_mapper import SensorMapper
        return [SensorMapper.init_scalar(item) for item in mongo_native.get_sensors_by_location_id(self.id)]

    @staticmethod
    def init_scalar(item):
        return LocationMapper(id = str(item['_id']), name = item['name'])