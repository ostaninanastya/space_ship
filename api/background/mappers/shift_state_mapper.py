import sys, os
import graphene
from neomodel import config
from person_mapper import PersonMapper
from shift_mapper import ShiftMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter
import neo4j_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/entities/')

from shift import Shift

import configparser

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

configp = configparser.ConfigParser()
configp.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

NEO4J_DB_URL = os.environ.get('NEO4J_DB_URL') if os.environ.get('NEO4J_DB_URL') else configp['NEO4J']['host']
NEO4J_DB_PORT = int(os.environ.get('NEO4J_DB_PORT') if os.environ.get('NEO4J_DB_PORT') else configp['NEO4J']['port'])

USERNAME = os.environ.get('NEO4J_DB_USERNAME') if os.environ.get('NEO4J_DB_USERNAME') else configp['NEO4J']['username']
PASSWORD = os.environ.get('NEO4J_DB_PASSWORD') if os.environ.get('NEO4J_DB_PASSWORD') else configp['NEO4J']['password']

config.DATABASE_URL = 'bolt://' + USERNAME + ':' + PASSWORD + '@' + NEO4J_DB_URL + ':' + str(NEO4J_DB_PORT)

class ShiftStateMapper(graphene.ObjectType):
    
    date = graphene.String()
    time = graphene.String()
    
    shiftid = graphene.String()
    warninglevel = graphene.String()

    remainingcartridges = graphene.Int()
    remainingair = graphene.Int()
    remainingelectricity = graphene.Int()

    shift = graphene.Field(ShiftMapper)

    comment = graphene.String()

    def resolve_shift(self, info):
        return ShiftMapper.init_scalar(Shift.nodes.get(ident = self.shiftid))

    @staticmethod
    def init_scalar(item):
        return ShiftStateMapper(date = date_to_str(item['date']),\
                                 time = time_to_str(item['time']),\
                                 shiftid = item['shift_id'].hex(),\
                                 warninglevel = item['warning_level'],\
                                 remainingcartridges = item['remaining_cartridges'],\
                                 remainingelectricity = item['remaining_electricity'],\
                                 remainingair = item['remaining_air'],\
                                 comment = item['comment'])