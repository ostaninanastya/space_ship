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

class UpdateSystemStates(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        description = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_description = graphene.String(default_value = '')

    ok = graphene.Boolean()
    system_states = graphene.List(lambda: SystemStateMapper)

    def mutate(self, info, id, name, description, set_name, set_description):
        #print('omg')
        system_states = [SystemStateMapper.init_scalar(item) for item in \
        mongo_native.update_system_states(_id = ObjectId(id) if id else None, name = name, description = description,
        set_name = set_name, set_description = set_description)]
        ok = True
        return UpdateSystemStates(system_states = system_states, ok = ok)