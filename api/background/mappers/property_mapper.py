import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

from property_type_mapper import PropertyTypeMapper
from department_mapper import DepartmentMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')
from data_adapters import parse_timestamp_parameter

class PropertyMapper(graphene.ObjectType):
    
    id = graphene.String()
    
    name = graphene.String()
    admission = graphene.String()
    comissioning = graphene.String()
    type = graphene.Field(lambda: PropertyTypeMapper)
    department = graphene.Field(lambda: DepartmentMapper)

    def resolve_type(self, info):
        return PropertyTypeMapper.init_scalar(mongo_mediator.get_property_type_by_id(self.type))

    def resolve_department(self, info):
        return DepartmentMapper.init_scalar(mongo_mediator.get_department_by_id(self.department))

    @staticmethod
    def eject(id, name, type, admission, comissioning, department):
        return [PropertyMapper.init_scalar(item) for item in mongo_mediator.select_properties(name = name, 
            admission = parse_timestamp_parameter(admission), comissioning = parse_timestamp_parameter(comissioning), 
            ids = {'_id': id, 'type': type, 'department': department})]

    @staticmethod
    def init_scalar(item):
        return PropertyMapper(id = str(item['_id']), name = item['name'], department = item['department'], 
            type = item['type'], comissioning = str(item['comissioning']), admission = str(item['admission']))
