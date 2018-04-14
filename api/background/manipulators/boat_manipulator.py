import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from boat_mapper import BoatMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class CreateBoat(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        capacity = graphene.Int()

    ok = graphene.Boolean()
    boat = graphene.Field(lambda: BoatMapper)

    def mutate(self, info, name, capacity):
        #print('omg')
        boat = BoatMapper.init_scalar(mongo_native.create_boat(name, capacity))
        ok = True
        return CreateBoat(boat = boat, ok = ok)

class RemoveBoat(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    boat = graphene.Field(lambda: BoatMapper)

    def mutate(self, info, id):
        boat = BoatMapper.init_scalar(mongo_native.remove_boat(id))
        ok = True
        return RemoveBoat(boat = boat, ok = ok)