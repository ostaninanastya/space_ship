import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from control_action_mapper import ControlActionMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import string_to_bytes, parse_timestamp_parameter, parse_objectid_parameter, parse_bytes_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/entities')

from control_action import ControlAction

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class CreateControlAction(graphene.Mutation):
    class Arguments:
        
        timestamp = graphene.String()
        mac = graphene.String()
        user = graphene.String()
        command = graphene.String()
        params = graphene.String()
        result = graphene.String()

    ok = graphene.Boolean()
    control_action = graphene.Field(lambda: ControlActionMapper)

    def mutate(self, info, timestamp, mac, user, command, params, result):
        control_action = ControlActionMapper.init_scalar(mongo_mediator.create_control_action(parse_timestamp_parameter(timestamp),
            parse_bytes_parameter(mac), parse_objectid_parameter(user), command, params, result))
        ok = True
        return CreateControlAction(control_action = control_action, ok = ok)

class RemoveControlAction(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    control_action = graphene.Field(lambda: ControlActionMapper)

    def mutate(self, info, timestamp):
        control_action = ControlActionMapper.init_scalar(mongo_mediator.remove_control_action(id))
        ok = True
        return RemoveControlAction(control_action = control_action, ok = ok)

class UpdateControlActions(graphene.Mutation):
    class Arguments:

        id = graphene.String(default_value = '')
        timestamp = graphene.String(default_value = '')
        mac = graphene.String(default_value = '')
        user = graphene.String(default_value = '')
        command = graphene.String(default_value = '')
        params = graphene.String(default_value = '')
        result = graphene.String(default_value = '')

        set_mac = graphene.String(default_value = '')
        set_user = graphene.String(default_value = '')
        set_command = graphene.String(default_value = '')
        set_params = graphene.String(default_value = '')
        set_result = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, id, timestamp, mac, user, command, params, result, set_mac, set_user, set_command, set_params, set_result):
        cassandra_mediator.update_control_actions(id = parse_objectid_parameter(id), timestamp = parse_timestamp_parameter(timestamp),
            user = parse_objectid_parameter(user), mac_address = parse_bytes_parameter(mac), command = command, params = params, result = result, 
            set_user_id = parse_objectid_parameter(set_user), set_mac_address = parse_bytes_parameter(set_mac),
            set_command = set_command, set_params = set_params, set_result = set_result)
        ok = True
        return UpdateControlActions(ok = ok)