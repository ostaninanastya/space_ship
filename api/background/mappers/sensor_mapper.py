import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

class SensorMapper(graphene.ObjectType):
	id = graphene.String()
	name = graphene.String()
	location = graphene.String()

	def resolve_name(self, info):
		return mongo_adapter.get_name_by_id('source_test', self.id)

	def resolce_location(self, info):
		return mongo_adapter.get_sensor_location_by_id('source_test', self.id)