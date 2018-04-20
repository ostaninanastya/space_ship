import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

from system_state_mapper import SystemStateMapper
from system_type_mapper import SystemTypeMapper
from person_mapper import PersonMapper

class SystemMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    
    serialnumber = graphene.Float()

    launched = graphene.String()
    checked = graphene.String()

    state = graphene.Field(lambda: SystemStateMapper)
    supervisor = graphene.Field(lambda: PersonMapper)
    type = graphene.Field(lambda: SystemTypeMapper)

    def resolve_state(self, info):
        return SystemStateMapper.init_scalar(mongo_native.get_system_state_by_id(self.state))

    def resolve_supervisor(self, info):
        return PersonMapper.init_scalar(mongo_native.get_person_by_id(self.supervisor))

    def resolve_type(self, info):
        return SystemTypeMapper.init_scalar(mongo_native.get_system_type_by_id(self.type))

    @staticmethod
    def init_scalar(item):
        return SystemMapper(id = str(item['_id']), 
            name = item['name'], 
            serialnumber = item['serial_number'], 
            launched = item['launched'], 
            checked = item['checked'],
            state = str(item['state']),
            supervisor = str(item['supervisor']),
            type = str(item['type']))

    '''
    def resolve_name(self, info):
    	return mongo_adapter.get_name_by_id('spec_test', self.id)

    def resolve_people(self, info):
    	from person_mapper import PersonMapper
    	return [PersonMapper(id = id) for id in mongo_native.get_people_ids_with_spec(self.id)]
    '''
    #db.sys_test.insert({'name':'first system', 'serial_number':13.12, 'launched':new Date("2016-09-18T16:00:00Z"), 'checked':new Date("2016-12-18T16:00:00Z"), 'state':ObjectId("5acd04b1ee18bbcfe8035ade"), 'supervisor':ObjectId("5ac8a53e1767171855a9dd89"), 'type':ObjectId("5acd0652ee18bbcfe8035adf")})