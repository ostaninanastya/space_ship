import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from shift_state_mapper import ShiftStateMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateShiftState(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()
        shift = graphene.String()
        warninglevel = graphene.String()
    
        remainingcartridges = graphene.Int()
        remainingair = graphene.Int()
        remainingelectricity = graphene.Int()

        comment = graphene.String()

    ok = graphene.Boolean()
    shiftstate = graphene.Field(lambda: ShiftStateMapper)

    def mutate(self, info, timestamp, shift, warninglevel, remainingcartridges, remainingair, remainingelectricity, comment):
        shiftstate = ShiftStateMapper.init_scalar(cassandra_mediator.create_shift_state(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN),\
            shift, warninglevel, remainingcartridges, remainingair, remainingelectricity, comment))
        ok = True
        return CreateShiftState(shiftstate = shiftstate, ok = ok)

class RemoveShiftState(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()

    ok = graphene.Boolean()
    shiftstate = graphene.Field(lambda: ShiftStateMapper)

    def mutate(self, info, timestamp):
        shiftstate = ShiftStateMapper.init_scalar(cassandra_mediator.remove_shift_state(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)))
        ok = True
        return RemoveShiftState(shiftstate = shiftstate, ok = ok)