import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

class SystemStateMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    description = graphene.String()

    systems = graphene.List('system_mapper.SystemMapper')

    def resolve_systems(self, info):
        from system_mapper import SystemMapper
        return [SystemMapper.init_scalar(item) for item in mongo_native.get_systems_by_state_id(self.id)]

    @staticmethod
    def init_scalar(item):
        return SystemStateMapper(id = str(item['_id']), name = item['name'], description = item['description'])

    '''
    def resolve_name(self, info):
    	return mongo_adapter.get_name_by_id('spec_test', self.id)

    def resolve_people(self, info):
    	from person_mapper import PersonMapper
    	return [PersonMapper(id = id) for id in mongo_native.get_people_ids_with_spec(self.id)]
    '''