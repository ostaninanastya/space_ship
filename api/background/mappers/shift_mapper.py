import sys, os
from neomodel import config
import graphene

from person_mapper import PersonMapper
from requirement_mapper import RequirementMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')
from data_adapters import parse_timestamp_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/')

import neo4j_mediator

class ShiftMapper(graphene.ObjectType):
    
    id = graphene.String()

    start = graphene.String()
    end = graphene.String()
    chief = graphene.Field(PersonMapper)
    workers = graphene.List(PersonMapper)
    requirements = graphene.List(RequirementMapper)

    def resolve_requirements(self, info):
        return [RequirementMapper.init_scalar(item) for item in neo4j_mediator.get_shift_requirements(self.id)]

    def resolve_chief(self, info):
        return PersonMapper.init_scalar(mongo_mediator.get_person_by_id(id = neo4j_mediator.get_shift_chief_id(self.id)))

    def resolve_workers(self, info):
        return [PersonMapper.init_scalar(mongo_mediator.get_person_by_id(worker_id)) for worker_id in neo4j_mediator.get_workers_id(self.id)]

    @staticmethod
    def eject(id, start, end):
        return [ShiftMapper.init_scalar(item) for item in neo4j_mediator.select_shifts(
                start = parse_timestamp_parameter(start), end = parse_timestamp_parameter(end), id = id)]

    @staticmethod
    def init_scalar(item):
        return ShiftMapper(id = item.ident,
                           start = str(item.start),
                           end = str(item.end))