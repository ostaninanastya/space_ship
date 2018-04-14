import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from location_mapper import LocationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class CreateLocation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    location = graphene.Field(lambda: LocationMapper)

    def mutate(self, info, name):
        location = LocationMapper.init_scalar(mongo_native.create_location(name))
        ok = True
        return CreateLocation(location = location, ok = ok)

class RemoveLocation(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    location = graphene.Field(lambda: LocationMapper)

    def mutate(self, info, id):
        location = LocationMapper.init_scalar(mongo_native.remove_location(id))
        ok = True
        return RemoveLocation(location = location, ok = ok)

class EradicateLocation(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    location = graphene.Field(lambda: LocationMapper)

    def mutate(self, info, id):
        location = LocationMapper.init_scalar(mongo_native.eradicate_location(id))
        ok = True
        return EradicateLocation(location = location, ok = ok)