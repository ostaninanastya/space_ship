import sys, os
import graphene

from specialization_mapper import SpecializationMapper
from department_mapper import DepartmentMapper

#import operation_mapper
#from . import OperationMapper

#from operation_mapper import OperationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import neo4j_adapter
import mongo_adapter

#print(dir(operation_mapper))

class PersonMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()

    department = graphene.Field(DepartmentMapper)

    directing = graphene.List(DepartmentMapper)

    chiefed = graphene.List('shift_mapper.ShiftMapper')
    worked = graphene.List('shift_mapper.ShiftMapper')

    headed = graphene.List('operation_mapper.OperationMapper')
    executed = graphene.List('operation_mapper.OperationMapper')

    specialization = graphene.Field(SpecializationMapper)

    def resolve_directing(self, info):
        return [DepartmentMapper(id = deparment_id) for deparment_id in neo4j_adapter.get_directed_ids(self.id)]

    def resolve_department(self, info):
        return DepartmentMapper(id = mongo_adapter.get_property_by_id('people_test', self.id, 'department'))
    
    def resolve_chiefed(self, info):
        from shift_mapper import ShiftMapper
        return [ShiftMapper(id = node['ident'],\
        				    start = str(node['start']),\
        				    end = str(node['end']))\
        		for node in neo4j_adapter.get_chiefed_shifts(self.id)]

    def resolve_worked(self, info):
        from shift_mapper import ShiftMapper
        return [ShiftMapper(id = node['ident'],\
        				    start = str(node['start']),\
        				    end = str(node['end']))\
        		for node in neo4j_adapter.get_worked_shifts(self.id)]

    def resolve_headed(self, info):
        from operation_mapper import OperationMapper
        return [OperationMapper(id = node['ident'],\
    						   name = node['name'],\
        					   start = str(node['start']),\
        					   end = str(node['end']))\
        		for node in neo4j_adapter.get_headed_operations(self.id)]

    def resolve_executed(self, info):
        from operation_mapper import OperationMapper
        return [OperationMapper(id = node['ident'],\
    						   name = node['name'],\
        					   start = str(node['start']),\
        					   end = str(node['end']))\
        		for node in neo4j_adapter.get_executed_operations(self.id)]

    def resolve_name(self, info):
        return mongo_adapter.get_name_by_id('people_test', self.id)

    def resolve_specialization(self, info):
        return SpecializationMapper(id = mongo_adapter.get_property_by_id('people_test', self.id, 'specialization'))