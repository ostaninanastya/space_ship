import sys, os, datetime
import graphene
from bson.objectid import ObjectId

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import parse_bytes_parameter, parse_timestamp_parameter, stringify_timestamp_parameter, parse_objectid_parameter

from person_mapper import PersonMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class ControlActionMapper(graphene.ObjectType):
    
    id = graphene.String()
    timestamp = graphene.String()

    mac = graphene.String()
    user = graphene.Field(lambda: PersonMapper)
    command = graphene.String()
    params = graphene.String()
    result = graphene.String()

    def resolve_user(self, info):
        return PersonMapper.init_scalar(mongo_mediator.get_person_by_id(self.user))

    @staticmethod
    def eject(id, timestamp, mac, user, command, params, result):
        return [ControlActionMapper.init_scalar(item) for item in mongo_mediator.select_control_actions(
            timestamp = parse_timestamp_parameter(timestamp),
            mac_address = parse_bytes_parameter(mac),
            user = parse_bytes_parameter(user),
            command = command, params = params, result = result, ids = {'_id': id})] 

    @staticmethod
    def init_scalar(item):
        return ControlActionMapper.init_scalar_dict(item)

    @staticmethod
    def init_scalar_dict(item):
        return ControlActionMapper(id = str(item['_id']),
                                   timestamp = stringify_timestamp_parameter(item['timestamp']),
                                   mac = item['mac_address'].hex(),
                                   command = item['command'],
                                   params = item['params'],
                                   result = item['result'],
                                   user = str(item['user']))