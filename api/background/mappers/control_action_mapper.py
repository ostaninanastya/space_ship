import sys, os, datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator
from data_adapters import parse_bytes_parameter, parse_date_parameter, parse_time_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

from person_mapper import PersonMapper

class ControlActionMapper(graphene.ObjectType):
    
    date = graphene.String()
    time = graphene.String()

    macaddress = graphene.String()
    user = graphene.Field(lambda: PersonMapper)
    command = graphene.String()
    params = graphene.String()
    result = graphene.String()

    def resolve_user(self, info):
        return PersonMapper.init_scalar(mongo_mediator.get_person_by_id(self.user))

    @staticmethod
    def eject(date, time, mac, user, command, params, result):
        return [ControlActionMapper.init_scalar(item) for item in cassandra_mediator.select_control_actions(
            date = parse_date_parameter(date),
            time = parse_time_parameter(time),
            mac_address = parse_bytes_parameter(mac), 
            user_id = parse_bytes_parameter(user), 
            command = command, params = params, result = result)] 

    @staticmethod
    def init_scalar(item):
        return ControlActionMapper(date = date_to_str(item.date), 
                                   time = time_to_str(item.time),
                                   macaddress = item.mac_address.hex(),
                                   command = item.command,
                                   params = item.params,
                                   result = item.result,
                                   user = item.user_id.hex())

    @staticmethod
    def init_scalar_dict(item):
        return ControlActionMapper(date = date_to_str(item['date']), 
                                   time = time_to_str(item['time']),
                                   macaddress = item['mac_address'].hex(),
                                   command = item['command'],
                                   params = item['params'],
                                   result = item['result'],
                                   user = item['user_id'].hex())