import sys, os

import graphene

from location_mapper import LocationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class SensorMapper(graphene.ObjectType):
	
	id = graphene.String()
	
	name = graphene.String()
	location = graphene.Field(lambda: LocationMapper)
	
	def resolve_location(self, info):
		return LocationMapper.init_scalar(mongo_mediator.get_location_by_id(self.location))

	@staticmethod
	def eject(id, name, location):
		return [SensorMapper.init_scalar(item) for item in mongo_mediator.select_sensors(name = name, ids = {'_id': id, 'location': location})]
	
	@staticmethod
	def init_scalar(item):
		return SensorMapper(id = str(item['_id']), name = item['name'], location = item.get('location'))