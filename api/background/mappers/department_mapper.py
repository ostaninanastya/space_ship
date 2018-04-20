import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter
import neo4j_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

import configparser

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

DEPARTMENTS_COLLECTION_NAME = os.environ.get('DEPARTMENTS_COLLECTION_NAME') or config['MONGO']['departments_collection_name']

class DepartmentMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    director = graphene.Field('person_mapper.PersonMapper')
    vk = graphene.String()
    properties = graphene.List('property_mapper.PropertyMapper')
    people = graphene.List('person_mapper.PersonMapper')

    @staticmethod
    def init_scalar(item):
        return DepartmentMapper(id = str(item['_id']), name = item['name'], vk = item.get('vk'))

    def resolve_name(self, info):
    	return mongo_adapter.get_name_by_id(DEPARTMENTS_COLLECTION_NAME, self.id)

    def resolve_vk(self, info):
    	return mongo_adapter.get_property_by_id(DEPARTMENTS_COLLECTION_NAME, self.id, 'vk')

    def resolve_director(self, info):
    	from person_mapper import PersonMapper
    	return PersonMapper(id = neo4j_adapter.get_director_id(self.id))

    def resolve_properties(self, info):
    	from property_mapper import PropertyMapper
    	return [PropertyMapper.init_scalar(item) for item in mongo_native.get_properties_with_department(self.id)]

    def resolve_people(self, info):
        from person_mapper import PersonMapper
        return [PersonMapper(id = id) for id in mongo_native.get_people_ids_with_dep(self.id)]


#db.people_test.update({}, {$set:{department:ObjectId("5ac5134ccc314386b6f43440")}});