import sys, os
from bson.objectid import ObjectId
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from system_type_mapper import SystemTypeMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class CreateSystemType(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String(default_value = '')

    ok = graphene.Boolean()
    system_type = graphene.Field(lambda: SystemTypeMapper)

    def mutate(self, info, name, description):
        system_type = SystemTypeMapper.init_scalar(mongo_mediator.create_system_type(name, description))
        ok = True
        return CreateSystemType(system_type = system_type, ok = ok)

class RemoveSystemType(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    system_type = graphene.Field(lambda: SystemTypeMapper)

    def mutate(self, info, id):
        system_type = SystemTypeMapper.init_scalar(mongo_mediator.remove_system_type(id))
        ok = True
        return RemoveSystemType(system_type = system_type, ok = ok)

class EradicateSystemType(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    system_type = graphene.Field(lambda: SystemTypeMapper)

    def mutate(self, info, id):
        system_type = SystemTypeMapper.init_scalar(mongo_mediator.eradicate_system_type(id))
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
        system_types = [SystemTypeMapper.init_scalar(item) for item in\
        mongo_mediator.update_system_types(_id = ObjectId(id) if id else None, name = name, description = description,
        set_name = set_name, set_description = set_description)]
        ok = True
        return UpdateSystemTypes(system_types = system_types, ok = ok)