import sys, os
from neomodel import config
import graphene
import json

from person_mapper import PersonMapper
from requirement_mapper import RequirementMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import parse_timestamp_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/')

import neo4j_mediator

class OperationMapper(graphene.ObjectType):
    
    id = graphene.String()
    
    name = graphene.String()
    start = graphene.String()
    end = graphene.String()
    head = graphene.Field(PersonMapper)
    executors = graphene.List(PersonMapper)
    requirements = graphene.List(RequirementMapper)

    def resolve_requirements(self, info):
        return [RequirementMapper.init_scalar(item) for item in neo4j_mediator.get_operation_requirements(self.id)]

    def resolve_head(self, info):
        return PersonMapper.init_scalar(mongo_mediator.get_person_by_id(id = neo4j_mediator.get_operation_head_id(self.id)))

    def resolve_executors(self, info):
        return [PersonMapper.init_scalar(mongo_mediator.get_person_by_id(executor_id)) for executor_id in neo4j_mediator.get_executors_id(self.id)]

    @staticmethod
    def eject(id, name, start, end):
        return [OperationMapper.init_scalar(item) for item in neo4j_mediator.select_operations(name__regex = '.*' + name + '.*',
                start = parse_timestamp_parameter(start), end = parse_timestamp_parameter(end), id = id)]

    @staticmethod
    def init_scalar(item):
        return OperationMapper(id = item.ident,
                               name = item.name,
                               start = str(item.start),
                               end = str(item.end))