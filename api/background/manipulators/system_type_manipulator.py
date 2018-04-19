import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from system_type_mapper import SystemTypeMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class CreateSystemType(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    system_type = graphene.Field(lambda: SystemTypeMapper)

    def mutate(self, info, name, description):
        #print('omg')
        system_type = SystemTypeMapper.init_scalar(mongo_native.create_system_type(name, description))
        ok = True
        return CreateSystemType(system_type = system_type, ok = ok)

class RemoveSystemType(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    system_type = graphene.Field(lambda: SystemTypeMapper)

    def mutate(self, info, id):
        system_type = SystemTypeMapper.init_scalar(mongo_native.remove_system_type(id))
        ok = True
        return RemoveSystemType(system_type = system_type, ok = ok)

class EradicateSystemType(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    system_type = graphene.Field(lambda: SystemTypeMapper)

    def mutate(self, info, id):
        system_type = SystemTypeMapper(id = id)
        mongo_native.eradicate_system_type(id)
        ok = True
        return EradicateSystemType(system_type = system_type, ok = ok)

class UpdateSystemTypes(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        description = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_description = graphene.String(default_value = '')

    ok = graphene.Boolean()
    system_types = graphene.List(lambda: SystemTypeMapper)

    def mutate(self, info, id, name, description, set_name, set_description):
        #print('omg')
        system_types = [SystemTypeMapper.init_scalar(item) for item in\
        mongo_native.update_system_types(_id = ObjectId(id) if id else None, name = name, description = description,
        set_name = set_name, set_description = set_description)]
        ok = True
        return UpdateSystemTypes(system_types = system_types, ok = ok)