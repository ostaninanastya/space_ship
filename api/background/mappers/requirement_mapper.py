import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

from requirement_entry_mapper import RequirementEntryMapper

class RequirementMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    content = graphene.List(RequirementEntryMapper)