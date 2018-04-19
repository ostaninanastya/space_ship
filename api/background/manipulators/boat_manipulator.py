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

class UpdateBoats(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        capacity = graphene.Int(default_value = -1)

        set_name = graphene.String(default_value = '')
        set_capacity = graphene.Int(default_value = -1)

    ok = graphene.Boolean()
    boats = graphene.List(lambda: BoatMapper)

    def mutate(self, info, id, name, capacity, set_name, set_capacity):
        #print('omg')
        boats = [BoatMapper.init_scalar(item) for item in mongo_native.update_boats(_id = ObjectId(id) if id else None, name = name, 
            capacity = capacity if capacity != -1 else None, set_name = set_name, set_capacity = set_capacity if set_capacity != -1 else None)]
        ok = True
        return UpdateBoats(boats = boats, ok = ok)