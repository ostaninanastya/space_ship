import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class SpecializationMapper(graphene.ObjectType):
    
    id = graphene.String()
    
    name = graphene.String()
    people = graphene.List('person_mapper.PersonMapper')

    def resolve_people(self, info):
    	from person_mapper import PersonMapper
    	return [PersonMapper.init_scalar(item) for item in mongo_mediator.get_people_with_specialization(self.id)]

    @staticmethod
    def eject(id, name):
        return [SpecializationMapper.init_scalar(item) for item in mongo_mediator.select_specializations(name = name, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        return SpecializationMapper(id = str(item['_id']), name = item['name'])