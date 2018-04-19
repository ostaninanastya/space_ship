import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class SpecializationMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    people = graphene.List('person_mapper.PersonMapper')

    def resolve_name(self, info):
    	if not self.name:
    		return mongo_adapter.get_name_by_id('spec_test', self.id)
    	return self.name

    def resolve_people(self, info):
    	from person_mapper import PersonMapper
    	return [PersonMapper(id = id) for id in mongo_native.get_people_ids_with_spec(self.id)]

    @staticmethod
    def init_scalar(item):
        return SpecializationMapper(id = str(item['_id']), name = item['name'])