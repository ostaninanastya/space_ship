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

class UpdateShifts(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        start = graphene.String(default_value = '')
        end = graphene.String(default_value = '')
        chief = graphene.String(default_value = '')
        workers = graphene.String(default_value = '')
        requirements = graphene.String(default_value = '')

        set_start = graphene.String(default_value = '')
        set_end = graphene.String(default_value = '')
        set_chief = graphene.String(default_value = '')
        set_rookies = graphene.String(default_value = '')
        set_dismissed = graphene.String(default_value = '')
        set_toughenings = graphene.String(default_value = '')
        set_softenings = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, id, chief, start, end, workers, requirements, set_chief, set_start, set_end, set_rookies, set_dismissed, set_toughenings, set_softenings):
        neo4j_mediator.update_shifts(ident = id,
            cheif = chief,
            start = None if not start else datetime.datetime.strptime(start, TIMESTAMP_PATTERN), 
            end = None if not end else datetime.datetime.strptime(end, TIMESTAMP_PATTERN), 
            workers = workers, requirements = requirements,
            set_chief = set_chief, set_start = None if not set_start else datetime.datetime.strptime(set_start, TIMESTAMP_PATTERN), 
            set_end = None if not set_end else datetime.datetime.strptime(set_end, TIMESTAMP_PATTERN), rookies = set_rookies, dismissed = set_dismissed, 
            toughenings = set_toughenings, softenings = set_softenings
        )
        ok = True
        return UpdateShifts(ok = ok)