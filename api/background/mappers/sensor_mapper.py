import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

from location_mapper import LocationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class SensorMapper(graphene.ObjectType):
	id = graphene.String()
	name = graphene.String()
	location = graphene.Field(lambda: LocationMapper)

	'''
	def resolve_name(self, info):
		return mongo_adapter.get_name_by_id('source_test', self.id)
	'''
	
	def resolve_location(self, info):
		return LocationMapper.init_scalar(mongo_native.get_location_by_id(self.location))
		#return mongo_adapter.get_sensor_location_by_id('source_test', self.id)

	@staticmethod
	def init_scalar(item):
		return SensorMapper(id = str(item['_id']), name = item['name'], location = item.get('location'))