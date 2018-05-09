import sys, os
import graphene

from requirement_entry_mapper import RequirementEntryMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class RequirementMapper(graphene.ObjectType):
    
    id = graphene.String()
    
    name = graphene.String()
    content = graphene.List(RequirementEntryMapper)
    shifts = graphene.List('shift_mapper.ShiftMapper')
    operations = graphene.List('operation_mapper.OperationMapper')

    def resolve_operations(self, info):
    	from operation_mapper import OperationMapper
    	return [OperationMapper.init_scalar(item) for item in mongo_mediator.get_operations_with_requirement(self.id)]

    def resolve_shifts(self, info):
    	from shift_mapper import ShiftMapper
    	return [ShiftMapper.init_scalar(item) for item in mongo_mediator.get_shifts_with_requirement(self.id)]	

    def resolve_content(self, info):
    	return [RequirementEntryMapper.init_scalar(item) for item in self.content]

    @staticmethod
    def eject(id, name, specializations):
        return [RequirementMapper.init_scalar(item) for item in mongo_mediator.select_requirements(
            name = name, specializations = specializations, ids = {'_id': id})]

    @staticmethod
    def init_scalar(node):
        return RequirementMapper(
            content = node['content'],
            id = node['_id'],
            name = node['name']
        )