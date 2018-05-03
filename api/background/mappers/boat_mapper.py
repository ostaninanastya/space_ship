import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class BoatMapper(graphene.ObjectType):
    
    id = graphene.String()
    
    name = graphene.String()
    capacity = graphene.Int()

    @staticmethod
    def eject(id, name, capacity):
        return [BoatMapper.init_scalar(item) for item in mongo_mediator.select_boats(name = name, capacity = capacity, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        return BoatMapper(id = str(item['_id']), name = item['name'], capacity = item.get('capacity'))