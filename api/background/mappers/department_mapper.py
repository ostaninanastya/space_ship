import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/')

import neo4j_mediator

class DepartmentMapper(graphene.ObjectType):
    
    id = graphene.String()
    
    name = graphene.String()
    director = graphene.Field('person_mapper.PersonMapper')
    vk = graphene.String()
    properties = graphene.List('property_mapper.PropertyMapper')
    people = graphene.List('person_mapper.PersonMapper')

    def resolve_director(self, info):
    	from person_mapper import PersonMapper
    	return PersonMapper.init_scalar(mongo_mediator.get_person_by_id(neo4j_mediator.get_director_id(self.id)))

    def resolve_properties(self, info):
    	from property_mapper import PropertyMapper
    	return [PropertyMapper.init_scalar(item) for item in mongo_mediator.get_properties_with_department(self.id)]

    def resolve_people(self, info):
        from person_mapper import PersonMapper
        return [PersonMapper.init_scalar(item) for item in mongo_mediator.get_people_with_department(self.id)]

    @staticmethod
    def eject(id, name, vk):
        return [DepartmentMapper.init_scalar(item) for item in mongo_mediator.select_departments(name = name, vk = vk, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        return DepartmentMapper(id = str(item['_id']), name = item['name'], vk = item.get('vk'))


#db.people_test.update({}, {$set:{department:ObjectId("5ac5134ccc314386b6f43440")}});