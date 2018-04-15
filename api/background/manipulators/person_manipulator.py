import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from person_mapper import PersonMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        surname = graphene.String()
        patronymic = graphene.String(default_value = '')
        phone = graphene.String()

        department = graphene.String()
        specialization = graphene.String()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: PersonMapper)

    def mutate(self, info, name, surname, patronymic, phone, department, specialization):
        #print('omg')
        new_person = mongo_native.create_person(name, surname, patronymic, phone, department, specialization)
        person = PersonMapper(id = str(new_person['_id']))
        ok = True
        return CreatePerson(person = person, ok = ok)

class RemovePerson(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: PersonMapper)

    def mutate(self, info, id):
        deleted = mongo_native.remove_person(id)
        person = PersonMapper(id = id, name = deleted['name'])
        ok = True
        return RemovePerson(person = person, ok = ok)

class EradicatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: PersonMapper)

    def mutate(self, info, id):
        deleted = mongo_native.eradicate_person(id)
        person = PersonMapper(id = id, name = deleted['name'])
        ok = True
        return EradicatePerson(person = person, ok = ok)