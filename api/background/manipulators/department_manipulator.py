import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from department_mapper import DepartmentMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class CreateDepartment(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        vk = graphene.String(default_value = 'http://vk.com/')

    ok = graphene.Boolean()
    department = graphene.Field(lambda: DepartmentMapper)

    def mutate(self, info, name, vk):
        #print('omg')
        new_department = mongo_native.create_department(name, vk)
        department = DepartmentMapper(id = str(new_department['_id']))
        ok = True
        return CreateDepartment(department = department, ok = ok)

class RemoveDepartment(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    department = graphene.Field(lambda: DepartmentMapper)

    def mutate(self, info, id):
        department = DepartmentMapper(id = id)
        mongo_native.remove_department(id)
        ok = True
        return RemoveDepartment(department = department, ok = ok)

class EradicateDepartment(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    department = graphene.Field(lambda: DepartmentMapper)

    def mutate(self, info, id):
        department = DepartmentMapper(id = id)
        mongo_native.eradicate_department(id)
        ok = True
        return EradicateDepartment(department = department, ok = ok)

class UpdateDepartments(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        vk = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_vk = graphene.String(default_value = '')

    ok = graphene.Boolean()
    departments = graphene.List(lambda: DepartmentMapper)

    def mutate(self, info, id, name, vk, set_name, set_vk):
        #print('omg')
        new_departments = mongo_native.update_departments(_id = ObjectId(id) if id else None, name = name, vk = vk, set_name = set_name, set_vk = set_vk)
        departments = [DepartmentMapper.init_scalar(item) for item in new_departments]
        ok = True
        return UpdateDepartments(departments = departments, ok = ok)