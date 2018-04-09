import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

class SpecializationMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()

    def resolve_name(self, info):
    	return mongo_adapter.get_name_by_id('spec_test', self.id)