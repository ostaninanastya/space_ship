import sys, os
from neomodel import config
import graphene

from person_mapper import PersonMapper
from requirement_mapper import RequirementMapper
from requirement_entry_mapper import RequirementEntryMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import neo4j_adapter
import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/entities/')

from requirement import Requirement

import configparser

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

configp = configparser.ConfigParser()
configp.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

NEO4J_DB_URL = os.environ.get('NEO4J_DB_URL') if os.environ.get('NEO4J_DB_URL') else configp['NEO4J']['host']
NEO4J_DB_PORT = int(os.environ.get('NEO4J_DB_PORT') if os.environ.get('NEO4J_DB_PORT') else configp['NEO4J']['port'])

USERNAME = os.environ.get('NEO4J_DB_USERNAME') if os.environ.get('NEO4J_DB_USERNAME') else configp['NEO4J']['username']
PASSWORD = os.environ.get('NEO4J_DB_PASSWORD') if os.environ.get('NEO4J_DB_PASSWORD') else configp['NEO4J']['password']

config.DATABASE_URL = 'bolt://' + USERNAME + ':' + PASSWORD + '@' + NEO4J_DB_URL + ':' + str(NEO4J_DB_PORT)

class ShiftMapper(graphene.ObjectType):
    id = graphene.String()

    start = graphene.String()
    end = graphene.String()

    chief = graphene.Field(PersonMapper)
    workers = graphene.List(PersonMapper)

    requirements = graphene.List(RequirementMapper)

    def resolve_requirements(self, info):
        return [RequirementMapper.init_scalar(Requirement.nodes.get(ident = requirement_id)) for requirement_id in neo4j_adapter.get_shift_requirements_id(self.id)]

    def resolve_chief(self, info):
        return PersonMapper(id = neo4j_adapter.get_shift_chief_id(self.id))

    def resolve_workers(self, info):
        return [PersonMapper(id = worker_id) for worker_id in neo4j_adapter.get_workers_id(self.id)]

    @staticmethod
    def init_scalar(item):
        return ShiftMapper(id = item.ident,\
                           start = str(item.start),\
                           end = str(item.end))