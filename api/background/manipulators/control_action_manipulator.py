import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from control_action_mapper import ControlActionMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator
from data_adapters import string_to_bytes

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/entities')

from control_action import ControlAction

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

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
        control_action = ControlActionMapper.init_scalar(cassandra_mediator.create_control_action(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN),\
            mac, user, command, params, result))
        ok = True
        return CreateControlAction(control_action = control_action, ok = ok)

class RemoveControlAction(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()

    ok = graphene.Boolean()
    control_action = graphene.Field(lambda: ControlActionMapper)

    def mutate(self, info, timestamp):
        control_action = ControlActionMapper.init_scalar(cassandra_mediator.remove_control_action(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)))
        ok = True
        return RemoveControlAction(control_action = control_action, ok = ok)

class UpdateControlActions(graphene.Mutation):
    class Arguments:
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

    def mutate(self, info, timestamp, mac, user, command, params, result, set_mac, set_user, set_command, set_params, set_result):
        parsed_timestamp = None if not timestamp else datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)
        cassandra_mediator.update_control_actions(date = None if not parsed_timestamp else parsed_timestamp.date(),\
            time = None if not parsed_timestamp else parsed_timestamp.time(), user_id = None if not user else string_to_bytes(user),\
            mac_address = None if not mac else string_to_bytes(mac), command = command, params = params, result = result, 
            set_user_id = None if not set_user else ControlAction.validate_user_id(string_to_bytes(set_user)),\
            set_mac_address = None if not set_mac else ControlAction.validate_mac_address(string_to_bytes(set_mac)),\
            set_command = set_command, set_params = set_params, set_result = set_result)
        ok = True
        return UpdateControlActions(ok = ok)