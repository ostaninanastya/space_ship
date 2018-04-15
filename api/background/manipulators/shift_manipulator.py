import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from shift_mapper import ShiftMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations')

import neo4j_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateShift(graphene.Mutation):
    class Arguments:
        start = graphene.String()
        end = graphene.String()
        chief = graphene.String()
        department = graphene.String()
        workers = graphene.String()
        requirements = graphene.String()

    ok = graphene.Boolean()
    shift = graphene.Field(lambda: ShiftMapper)

    def mutate(self, info, start, end, department, chief, workers, requirements):
        shift = ShiftMapper.init_scalar(neo4j_mediator.create_shift(\
            chief, department, datetime.datetime.strptime(start, TIMESTAMP_PATTERN), datetime.datetime.strptime(end, TIMESTAMP_PATTERN), workers, requirements\
        ))
        ok = True
        return CreateShift(shift = shift, ok = ok)

class RemoveShift(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    shift = graphene.Field(lambda: ShiftMapper)

    def mutate(self, info, id):
        shift = ShiftMapper.init_scalar(neo4j_mediator.remove_shift(id))
        ok = True
        return RemoveShift(shift = shift, ok = ok)