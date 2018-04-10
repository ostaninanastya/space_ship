import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

from specialization_mapper import SpecializationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class PropertyTypeMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    description = graphene.String()
    properties = graphene.List('property_mapper.PropertyMapper')

    def resolve_properties(self, info):
    	from property_mapper import PropertyMapper
    	return [PropertyMapper.init_scalar(item) for item in mongo_native.get_properties_with_type(self.id)]

    @staticmethod
    def init_scalar(item):
    	return PropertyTypeMapper(id = str(item['_id']), name = item['name'], description = item['description'])
