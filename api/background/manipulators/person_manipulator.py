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

class UpdatePeople(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        surname = graphene.String(default_value = '')
        patronymic = graphene.String(default_value = '')
        phone = graphene.String(default_value = '')
        department = graphene.String(default_value = '')
        specialization = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_surname = graphene.String(default_value = '')
        set_patronymic = graphene.String(default_value = '')
        set_phone = graphene.String(default_value = '')
        set_department = graphene.String(default_value = '')
        set_specialization = graphene.String(default_value = '')

    ok = graphene.Boolean()
    people = graphene.List(lambda: PersonMapper)

    def mutate(self, info, id, name, surname, patronymic, phone, department, specialization, 
        set_name, set_surname, set_patronymic, set_phone, set_department, set_specialization):
        #print('omg')
        new_people = mongo_native.update_people(_id = ObjectId(id) if id else None, name = name, surname = surname, patronymic = patronymic,\
        phone = phone, department = ObjectId(department) if department else None, specialization = ObjectId(specialization) if specialization else None,
        set_name = set_name, set_surname = set_surname, set_patronymic = set_patronymic,\
        set_phone = set_phone, set_department = ObjectId(set_department) if set_department else None,\
        set_specialization = ObjectId(set_specialization) if set_specialization else None)
        people = [PersonMapper.init_scalar(item) for item in new_people]
        ok = True
        return UpdatePeople(people = people, ok = ok)