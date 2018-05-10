import sys, os
from bson.objectid import ObjectId

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from department_mapper import DepartmentMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class CreateDepartment(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        vk = graphene.String(default_value = 'http://vk.com/')
        director = graphene.String()

    ok = graphene.Boolean()
    department = graphene.Field(lambda: DepartmentMapper)

    def mutate(self, info, name, vk, director):
        #print('omg')
        department = None
        try:
            new_department = mongo_mediator.create_department(name, vk, director)
            department = DepartmentMapper.init_scalar(new_department)
            ok = True
        except IndexError:
            ok = False
        return CreateDepartment(department = department, ok = ok)

class RemoveDepartment(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    department = graphene.Field(lambda: DepartmentMapper)

    def mutate(self, info, id):
        department = DepartmentMapper.init_scalar(mongo_mediator.remove_department(id))
        ok = True
        return RemoveDepartment(department = department, ok = ok)

class EradicateDepartment(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    department = graphene.Field(lambda: DepartmentMapper)

    def mutate(self, info, id):
        department = DepartmentMapper(id = id)
        mongo_mediator.eradicate_department(id)
        ok = True
        return EradicateDepartment(department = department, ok = ok)

class UpdateDepartments(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        vk = graphene.String(default_value = '')
        director = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_vk = graphene.String(default_value = '')
        set_director = graphene.String(default_value = '')

    ok = graphene.Boolean()
    departments = graphene.List(lambda: DepartmentMapper)

    def mutate(self, info, id, director, name, vk, set_name, set_vk, set_director):
        #print('omg')
        departments = None
        try:
            new_departments = mongo_mediator.update_departments(_id = ObjectId(id) if id else None, name = name, vk = vk, 
                director = ObjectId(director) if director else None,
                set_name = set_name, set_vk = set_vk, set_director = ObjectId(set_director) if set_director else None)
            departments = [DepartmentMapper.init_scalar(item) for item in new_departments]
            ok = True
        except IndexError:
            ok = False
        return UpdateDepartments(departments = departments, ok = ok)