import sys, os
import configparser
import datetime
import graphene
from bson.objectid import ObjectId

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from shift_state_mapper import ShiftStateMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import string_to_bytes, parse_timestamp_parameter, parse_objectid_parameter, parse_bytes_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class CreateShiftState(graphene.Mutation):
    class Arguments:
        
        timestamp = graphene.String()
        shift = graphene.String()
        warninglevel = graphene.String()

        cartridges = graphene.Int()
        air = graphene.Int()
        electricity = graphene.Int()

        comment = graphene.String()

    ok = graphene.Boolean()
    shift_state = graphene.Field(lambda: ShiftStateMapper)

    def mutate(self, info, timestamp, shift, warninglevel, cartridges, air, electricity, comment):
        shift_state = None
        try:
            shift_state = ShiftStateMapper.init_scalar(mongo_mediator.create_shift_state(parse_timestamp_parameter(timestamp),
                parse_objectid_parameter(shift), warninglevel, cartridges, air, electricity, comment))
            ok = True
        except IndexError:
            ok = False
        return CreateShiftState(shift_state = shift_state, ok = ok)

class RemoveShiftState(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    shift_state = graphene.Field(lambda: ShiftStateMapper)

    def mutate(self, info, id):
        shift_state = ShiftStateMapper.init_scalar(mongo_mediator.remove_shift_state(id))
        ok = True
        return RemoveShiftState(shift_state = shift_state, ok = ok)

class UpdateShiftStates(graphene.Mutation):
    class Arguments:

        id = graphene.String(default_value = '')
        timestamp = graphene.String(default_value = '')
        shift = graphene.String(default_value = '')
        warninglevel = graphene.String(default_value = '')   
        cartridges = graphene.Int(default_value = -1)
        air = graphene.Int(default_value = -1)
        electricity = graphene.Int(default_value = -1)
        comment = graphene.String(default_value = '')

        set_shift = graphene.String(default_value = '')
        set_warninglevel = graphene.String(default_value = '')   
        set_cartridges = graphene.Int(default_value = -1)
        set_air = graphene.Int(default_value = -1)
        set_electricity = graphene.Int(default_value = -1)
        set_comment = graphene.String(default_value = '')
        set_timestamp = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, id, timestamp, shift, warninglevel, cartridges, air, electricity, comment,
        set_shift, set_warninglevel, set_cartridges, set_air, set_electricity, set_comment, set_timestamp):
        try:
            mongo_mediator.update_shift_states(_id = parse_objectid_parameter(id), timestamp = parse_timestamp_parameter(timestamp),
                shift = shift, warning_level = warninglevel, 
                cartridges = None if cartridges < 0 else cartridges, 
                air = None if air < 0 else air, 
                electricity = None if electricity < 0 else electricity, 
                comment = comment,
                set_shift = parse_objectid_parameter(set_shift), 
                set_warning_level = set_warninglevel, 
                set_cartridges = None if set_cartridges < 0 else set_cartridges,
                set_remaining_air = None if set_air < 0 else set_air,
                set_remaining_electricity = None if set_electricity < 0 else set_electricity,
                set_comment = set_comment, set_timestamp = parse_timestamp_parameter(set_timestamp))
            ok = True
        except IndexError:
            ok = False
        return UpdateShiftStates(ok = ok)