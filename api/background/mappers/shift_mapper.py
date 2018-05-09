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

class ShiftMapper(graphene.ObjectType):
    
    id = graphene.String()

    start = graphene.String()
    end = graphene.String()
    chief = graphene.Field(PersonMapper)
    workers = graphene.List(PersonMapper)
    requirements = graphene.List(RequirementMapper)

    def resolve_requirements(self, info):
        return [RequirementMapper.init_scalar(mongo_mediator.get_requirement_by_id(id = id)) for id in self.requirements]

    def resolve_chief(self, info):
        return PersonMapper.init_scalar(mongo_mediator.get_person_by_id(id = self.chief))

    def resolve_workers(self, info):
        return [PersonMapper.init_scalar(mongo_mediator.get_person_by_id(worker_id)) for worker_id in self.workers]

    @staticmethod
    def eject(id, start, end):
        return [ShiftMapper.init_scalar(item) for item in mongo_mediator.select_shifts(
                start = parse_timestamp_parameter(start), end = parse_timestamp_parameter(end), ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        return ShiftMapper(id = item['_id'],
                           start = str(item['start']),
                           end = str(item['end']),
                           chief = item['chief'],
                           workers = item['workers'],
                           requirements = item['requirements'])