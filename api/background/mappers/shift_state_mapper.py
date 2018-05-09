import sys, os, datetime
import graphene
from neomodel import config
from person_mapper import PersonMapper
from shift_mapper import ShiftMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import parse_bytes_parameter, parse_timestamp_parameter, stringify_timestamp_parameter, parse_objectid_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class ShiftStateMapper(graphene.ObjectType):
    
    id = graphene.String()
    timestamp = graphene.String()
    
    shift = graphene.Field(lambda: ShiftMapper)
    warninglevel = graphene.String()
    cartridges = graphene.Int()
    air = graphene.Int()
    electricity = graphene.Int()
    comment = graphene.String()

    def resolve_shift(self, info):
        return ShiftMapper.init_scalar(mongo_mediator.get_shift_by_id(self.shift))

    @staticmethod
    def eject(id, timestamp, shift, warninglevel, cartridges, air, electricity, comment):
        return [ShiftStateMapper.init_scalar(item) for item in mongo_mediator.select_shift_states(
            timestamp = parse_timestamp_parameter(timestamp),
            shift = parse_objectid_parameter(shift), 
            warning_level = warninglevel, cartridges = cartridges if cartridges > 0 else None, 
            air = air if air > 0 else None, electricity = electricity if electricity > 0 else None,
            comment = comment, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        return ShiftStateMapper(id = str(item['_id']),
                                timestamp = stringify_timestamp_parameter(item['timestamp']),
                                shift = str(item['shift']),
                                warninglevel = item['warning_level'],
                                cartridges = item['cartridges'],
                                electricity = item['electricity'],
                                air = item['air'],
                                comment = item['comment'])