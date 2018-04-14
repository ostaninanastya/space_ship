import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from specialization_mapper import SpecializationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class CreateSpecialization(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    specialization = graphene.Field(lambda: SpecializationMapper)

    def mutate(self, info, name):
        #print('omg')
        new_specialization = mongo_native.create_specialization(name)
        specialization = SpecializationMapper(id = str(new_specialization['_id']))
        ok = True
        return CreateSpecialization(specialization = specialization, ok = ok)

class RemoveSpecialization(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    specialization = graphene.Field(lambda: SpecializationMapper)

    def mutate(self, info, id):
        specialization = SpecializationMapper(id = id)
        mongo_native.remove_specialization(id)
        ok = True
        return RemoveSpecialization(specialization = specialization, ok = ok)

class Eradicate(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    specialization = graphene.Field(lambda: SpecializationMapper)

    def mutate(self, info, id):
        specialization = SpecializationMapper(id = id)
        mongo_native.eradicate_specialization(id)
        ok = True
        return Eradicate(specialization = specialization, ok = ok)