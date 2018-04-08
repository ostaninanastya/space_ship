import sys, os

import graphene

from person_mapper import PersonMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import neo4j_adapter
import mongo_adapter

class OperationMapper(graphene.ObjectType):
    name = graphene.String()
    id = graphene.String()

    start = graphene.String()
    end = graphene.String()

    director = graphene.Field(PersonMapper)


    def resolve_director(self, info):

        director_id = neo4j_adapter.get_operation_director_id(self.id)

        return PersonMapper(id = director_id,\
        					name = mongo_adapter.get_name_by_id('people_test', director_id))