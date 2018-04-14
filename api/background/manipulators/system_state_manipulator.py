import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from system_state_mapper import SystemStateMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class CreateSystemState(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    system_state = graphene.Field(lambda: SystemStateMapper)

    def mutate(self, info, name, description):
        #print('omg')
        system_state = SystemStateMapper.init_scalar(mongo_native.create_system_state(name, description))
        ok = True
        return CreateSystemState(system_state = system_state, ok = ok)

class RemoveSystemState(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    system_state = graphene.Field(lambda: SystemStateMapper)

    def mutate(self, info, id):
        system_state = SystemStateMapper.init_scalar(mongo_native.remove_system_state(id))
        ok = True
        return RemoveSystemState(system_state = system_state, ok = ok)

class EradicateSystemState(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    system_state = graphene.Field(lambda: SystemStateMapper)

    def mutate(self, info, id):
        system_state = SystemStateMapper(id = id)
        mongo_native.eradicate_system_state(id)
        ok = True
        return EradicateSystemState(system_state = system_state, ok = ok)