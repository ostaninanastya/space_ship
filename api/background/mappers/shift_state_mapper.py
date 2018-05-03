import sys, os, datetime
import graphene
from neomodel import config
from person_mapper import PersonMapper
from shift_mapper import ShiftMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator
from data_adapters import parse_bytes_parameter, parse_date_parameter, parse_time_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/')

import neo4j_mediator

class ShiftStateMapper(graphene.ObjectType):
    
    date = graphene.String()
    time = graphene.String()
    
    shift = graphene.Field(lambda: ShiftMapper)
    warninglevel = graphene.String()
    remainingcartridges = graphene.Int()
    remainingair = graphene.Int()
    remainingelectricity = graphene.Int()
    comment = graphene.String()

    def resolve_shift(self, info):
        return ShiftMapper.init_scalar(neo4j_mediator.get_shift_by_id(self.shift))

    @staticmethod
    def eject(date, time, shift, warninglevel, remainingcartridges, remainingair, remainingelectricity, comment):
        return [ShiftStateMapper.init_scalar(item) for item in cassandra_mediator.select_shift_states(
            date = parse_date_parameter(date),
            time = parse_time_parameter(time),
            shift_id = parse_bytes_parameter(shift), 
            warning_level = warninglevel, remaining_cartridges = remainingcartridges, remaining_air = remainingair, remaining_electricity = remainingelectricity,
            comment = comment)]

    @staticmethod
    def init_scalar(item):
        return ShiftStateMapper(date = date_to_str(item['date']),
                                time = time_to_str(item['time']),
                                shift = item['shift_id'].hex(),
                                warninglevel = item['warning_level'],
                                remainingcartridges = item['remaining_cartridges'],
                                remainingelectricity = item['remaining_electricity'],
                                remainingair = item['remaining_air'],
                                comment = item['comment'])