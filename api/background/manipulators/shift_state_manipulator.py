import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from shift_state_mapper import ShiftStateMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/entities')

from shift_state import ShiftState

import cassandra_mediator
from data_adapters import string_to_bytes

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

class UpdateShiftStates(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String(default_value = '')
        shift = graphene.String(default_value = '')
        warninglevel = graphene.String(default_value = '')   
        remainingcartridges = graphene.Int(default_value = -1)
        remainingair = graphene.Int(default_value = -1)
        remainingelectricity = graphene.Int(default_value = -1)
        comment = graphene.String(default_value = '')

        set_shift = graphene.String(default_value = '')
        set_warninglevel = graphene.String(default_value = '')   
        set_remainingcartridges = graphene.Int(default_value = -1)
        set_remainingair = graphene.Int(default_value = -1)
        set_remainingelectricity = graphene.Int(default_value = -1)
        set_comment = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, timestamp, shift, warninglevel, remainingcartridges, remainingair, remainingelectricity, comment,
        set_shift, set_warninglevel, set_remainingcartridges, set_remainingair, set_remainingelectricity, set_comment):
        parsed_timestamp = None if not timestamp else datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)
        cassandra_mediator.update_shift_state(date = None if not parsed_timestamp else parsed_timestamp.date,\
            time = None if not parsed_timestamp else parsed_timestamp.time,
            shift_id = shift, warning_level = warninglevel, remaining_cartridges = remainingcartridges, remaining_air = remainingair,
            remaining_electricity = remainingelectricity, comment = comment,
            set_shift_id = None if not set_shift else ShiftState.validate_shift_id(set_shift), 
            set_warning_level = None if not set_shift else ShiftState.validate_warning_level(set_warninglevel), 
            set_remaining_cartridges = None if set_remainingcartridges < 0 else ShiftState.validate_remaining_quantity(set_remainingcartridges, 'cart'),
            set_remaining_air = None if set_remainingair < 0 else ShiftState.validate_remaining_quantity(set_remainingair, 'air'),
            set_remaining_electricity = None if set_remainingelectricity < 0 else ShiftState.validate_remaining_quantity(set_remainingelectricity, 'e'),
            set_comment = set_comment)
        ok = True
        return UpdateShiftStates(ok = ok)