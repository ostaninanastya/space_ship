import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter
import neo4j_adapter

class DepartmentMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    director = graphene.Field('person_mapper.PersonMapper')

    def resolve_name(self, info):
    	return mongo_adapter.get_name_by_id('department_test', self.id)

    def resolve_director(self, info):
    	from person_mapper import PersonMapper
    	return PersonMapper(id = neo4j_adapter.get_director_id(self.id))


#db.people_test.update({}, {$set:{department:ObjectId("5ac5134ccc314386b6f43440")}});