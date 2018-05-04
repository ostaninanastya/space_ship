import sys, os
from bson.objectid import ObjectId

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from location_mapper import LocationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class CreateLocation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    location = graphene.Field(lambda: LocationMapper)

    def mutate(self, info, name):
        location = LocationMapper.init_scalar(mongo_mediator.create_location(name))
        ok = True
        return CreateLocation(location = location, ok = ok)

class RemoveLocation(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    location = graphene.Field(lambda: LocationMapper)

    def mutate(self, info, id):
        location = LocationMapper.init_scalar(mongo_mediator.remove_location(id))
        ok = True
        return RemoveLocation(location = location, ok = ok)

class EradicateLocation(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    location = graphene.Field(lambda: LocationMapper)

    def mutate(self, info, id):
        location = LocationMapper.init_scalar(mongo_mediator.eradicate_location(id))
        ok = True
        return EradicateLocation(location = location, ok = ok)

class UpdateLocations(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')

    ok = graphene.Boolean()
    locations = graphene.List(lambda: LocationMapper)

    def mutate(self, info, id, name, set_name):
        locations = [LocationMapper.init_scalar(item) for item in \
        mongo_mediator.update_locations(_id = ObjectId(id) if id else None, name = name, set_name = set_name)]
        ok = True
        return UpdateLocations(locations = locations, ok = ok)