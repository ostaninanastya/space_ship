import sys, os

import graphene

from person_mapper import PersonMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import neo4j_adapter
import mongo_adapter

class ShiftMapper(graphene.ObjectType):
    id = graphene.String()

    start = graphene.String()
    end = graphene.String()

    chief = graphene.Field(PersonMapper)

    def resolve_chief(self, info):

        chief_id = neo4j_adapter.get_shift_chief_id(self.id)

        return PersonMapper(id = chief_id,\
        					name = mongo_adapter.get_name_by_id('people_test', chief_id))