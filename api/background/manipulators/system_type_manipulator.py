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