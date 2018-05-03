import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

from system_state_mapper import SystemStateMapper
from system_type_mapper import SystemTypeMapper
from person_mapper import PersonMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')
from data_adapters import parse_timestamp_parameter, parse_float_parameter

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
        return SystemStateMapper.init_scalar(mongo_mediator.get_system_state_by_id(self.state))

    def resolve_supervisor(self, info):
        return PersonMapper.init_scalar(mongo_mediator.get_person_by_id(self.supervisor))

    def resolve_type(self, info):
        return SystemTypeMapper.init_scalar(mongo_mediator.get_system_type_by_id(self.type))

    @staticmethod
    def eject(id, name, launched, checked, serialnumber, state, type, supervisor):
        return [SystemMapper.init_scalar(item) for item in mongo_mediator.select_systems(name = name, 
            serialnumber = parse_float_parameter(serialnumber), launched = parse_timestamp_parameter(launched), checked = parse_timestamp_parameter(checked),
            ids = {'_id': id, 'state': state, 'type': type, 'supervisor': supervisor})]

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

#db.sys_test.insert({'name':'first system', 'serial_number':13.12, 'launched':new Date("2016-09-18T16:00:00Z"), 'checked':new Date("2016-12-18T16:00:00Z"), 'state':ObjectId("5acd04b1ee18bbcfe8035ade"), 'supervisor':ObjectId("5ac8a53e1767171855a9dd89"), 'type':ObjectId("5acd0652ee18bbcfe8035adf")})