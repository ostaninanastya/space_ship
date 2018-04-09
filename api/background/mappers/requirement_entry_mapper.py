import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

from specialization_mapper import SpecializationMapper

class RequirementEntryMapper(graphene.ObjectType):
    specialization = graphene.Field(lambda: SpecializationMapper)
    quantity = graphene.Int()

    def resolve_specialization(self, info):
    	return SpecializationMapper(id = self.specialization)
