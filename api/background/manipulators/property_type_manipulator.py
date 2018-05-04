import sys, os
from bson.objectid import ObjectId
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from property_type_mapper import PropertyTypeMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class CreatePropertyType(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String(default_value = '')

    ok = graphene.Boolean()
    property_type = graphene.Field(lambda: PropertyTypeMapper)

    def mutate(self, info, name, description):
        #print('omg')
        property_type = PropertyTypeMapper.init_scalar(mongo_mediator.create_property_type(name, description))
        ok = True
        return CreatePropertyType(property_type = property_type, ok = ok)

class RemovePropertyType(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    property_type = graphene.Field(lambda: PropertyTypeMapper)

    def mutate(self, info, id):
        property_type = PropertyTypeMapper.init_scalar(mongo_mediator.remove_property_type(id))
        ok = True
        return RemovePropertyType(property_type = property_type, ok = ok)

class EradicatePropertyType(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    property_type = graphene.Field(lambda: PropertyTypeMapper)

    def mutate(self, info, id):
        property_type = PropertyTypeMapper.init_scalar(mongo_mediator.eradicate_property_type(id))
        ok = True
        return EradicatePropertyType(property_type = property_type, ok = ok)

class UpdatePropertyTypes(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        description = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_description = graphene.String(default_value = '')

    ok = graphene.Boolean()
    property_types = graphene.List(lambda: PropertyTypeMapper)

    def mutate(self, info, id, name, description, set_name, set_description):
        #print('omg')
        property_types = [PropertyTypeMapper.init_scalar(item) for item in \
        mongo_mediator.update_property_types(_id = ObjectId(id) if id else None, name = name, description = description,
        set_name = set_name, set_description = set_description)]
        ok = True
        return UpdatePropertyTypes(property_types = property_types, ok = ok)