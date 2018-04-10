import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter
import neo4j_adapter

from requirement_entry_mapper import RequirementEntryMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/entities/')

from requirement import Requirement
from shift import Shift
from operation import Operation

class RequirementMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    content = graphene.List(RequirementEntryMapper)

    shifts = graphene.List('shift_mapper.ShiftMapper')
    operations = graphene.List('operation_mapper.OperationMapper')

    def resolve_operations(self, info):
    	from operation_mapper import OperationMapper
    	return [OperationMapper.init_scalar(Operation.nodes.get(ident = ident)) for ident in neo4j_adapter.get_operation_ids_by_requirement(self.id)]

    def resolve_shifts(self, info):
    	from shift_mapper import ShiftMapper
    	return [ShiftMapper.init_scalar(Shift.nodes.get(ident = ident)) for ident in neo4j_adapter.get_shift_ids_by_requirement(self.id)]	

    def resolve_content(self, info):
    	return [RequirementEntryMapper.init_scalar(item) for item in self.content]

    @staticmethod
    def init_scalar(node):
        print()
        return RequirementMapper(
            content = node.content,
            id = node.ident,
            name = node.name
        )