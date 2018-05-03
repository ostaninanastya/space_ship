import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class SystemStateMapper(graphene.ObjectType):
    
    id = graphene.String()
    
    name = graphene.String()
    description = graphene.String()
    systems = graphene.List('system_mapper.SystemMapper')

    def resolve_systems(self, info):
        from system_mapper import SystemMapper
        return [SystemMapper.init_scalar(item) for item in mongo_mediator.get_systems_by_state_id(self.id)]

    @staticmethod
    def eject(id, name, desc):
        return [SystemStateMapper.init_scalar(item) for item in mongo_mediator.select_system_states(name = name, description = desc, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        return SystemStateMapper(id = str(item['_id']), name = item['name'], description = item['description'])