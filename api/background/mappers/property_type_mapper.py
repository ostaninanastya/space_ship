import sys, os
import graphene

from specialization_mapper import SpecializationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class PropertyTypeMapper(graphene.ObjectType):
    
    id = graphene.String()
    
    name = graphene.String()
    description = graphene.String()
    properties = graphene.List('property_mapper.PropertyMapper')

    def resolve_properties(self, info):
    	from property_mapper import PropertyMapper
    	return [PropertyMapper.init_scalar(item) for item in mongo_mediator.get_properties_with_type(self.id)]

    @staticmethod
    def eject(id, name, desc):
        return [PropertyTypeMapper.init_scalar(item) for item in mongo_mediator.select_property_types(name = name, description = desc, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
    	return PropertyTypeMapper(id = str(item['_id']), name = item['name'], description = item['description'])
