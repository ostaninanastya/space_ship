import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class LocationMapper(graphene.ObjectType):
    
    id = graphene.String()
    
    name = graphene.String()
    sensors = graphene.List('sensor_mapper.SensorMapper')

    def resolve_sensors(self, info):
        from sensor_mapper import SensorMapper
        return [SensorMapper.init_scalar(item) for item in mongo_mediator.get_sensors_by_location_id(self.id)]

    @staticmethod
    def eject(id, name):
        return [LocationMapper.init_scalar(item) for item in mongo_mediator.select_locations(name = name, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        return LocationMapper(id = str(item['_id']), name = item['name'])