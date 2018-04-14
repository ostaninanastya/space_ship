import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from property_type_mapper import PropertyTypeMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class CreatePropertyType(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    property_type = graphene.Field(lambda: PropertyTypeMapper)

    def mutate(self, info, name, description):
        #print('omg')
        property_type = PropertyTypeMapper.init_scalar(mongo_native.create_property_type(name, description))
        ok = True
        return CreatePropertyType(property_type = property_type, ok = ok)

class RemovePropertyType(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    property_type = graphene.Field(lambda: PropertyTypeMapper)

    def mutate(self, info, id):
        property_type = PropertyTypeMapper.init_scalar(mongo_native.remove_property_type(id))
        ok = True
        return RemovePropertyType(property_type = property_type, ok = ok)

class EradicatePropertyType(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    property_type = graphene.Field(lambda: PropertyTypeMapper)

    def mutate(self, info, id):
        property_type = PropertyTypeMapper(id = id)
        mongo_native.eradicate_property_type(id)
        ok = True
        return EradicatePropertyType(property_type = property_type, ok = ok)