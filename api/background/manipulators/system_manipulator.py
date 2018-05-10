import sys, os, math
from bson.objectid import ObjectId
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from system_mapper import SystemMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateSystem(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        serialnumber = graphene.Float()
        launched = graphene.String()
        checked = graphene.String()
        state = graphene.String()
        supervisor = graphene.String()
        type = graphene.String()

    ok = graphene.Boolean()
    system = graphene.Field(lambda: SystemMapper)

    def mutate(self, info, name, serialnumber, launched, checked, state, supervisor, type):
        system = None
        try:
            system = SystemMapper.init_scalar(mongo_mediator.create_system(\
                name, serialnumber, datetime.datetime.strptime(launched, TIMESTAMP_PATTERN), datetime.datetime.strptime(checked, TIMESTAMP_PATTERN), state, supervisor, type\
            ))
            ok = True
        except IndexError:
            ok = False
        return CreateSystem(system = system, ok = ok)

class RemoveSystem(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    system = graphene.Field(lambda: SystemMapper)

    def mutate(self, info, id):
        system = SystemMapper.init_scalar(mongo_mediator.remove_system(id))
        ok = True
        return RemoveSystem(system = system, ok = ok)

class UpdateSystems(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        serialnumber = graphene.Float(default_value = float('nan'))
        launched = graphene.String(default_value = '')
        checked = graphene.String(default_value = '')
        state = graphene.String(default_value = '')
        supervisor = graphene.String(default_value = '')
        type = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_serialnumber = graphene.Float(default_value = float('nan'))
        set_launched = graphene.String(default_value = '')
        set_checked = graphene.String(default_value = '')
        set_state = graphene.String(default_value = '')
        set_supervisor = graphene.String(default_value = '')
        set_type = graphene.String(default_value = '')

    ok = graphene.Boolean()
    systems = graphene.List(lambda: SystemMapper)

    def mutate(self, info, id, name, serialnumber, launched, checked, state, supervisor, type, 
        set_name, set_serialnumber, set_launched, set_checked, set_state, set_supervisor, set_type):
        systems = None
        try:
            systems = [SystemMapper.init_scalar(item) for item in mongo_mediator.update_systems(\
                _id = ObjectId(id) if id else None, name = name, 
                serialnumber = serialnumber if not math.isnan(serialnumber) else None, 
                launched = datetime.datetime.strptime(launched, TIMESTAMP_PATTERN) if launched else None, 
                checked = datetime.datetime.strptime(checked, TIMESTAMP_PATTERN) if checked else None, 
                state = ObjectId(state) if state else None, supervisor = ObjectId(supervisor) if supervisor else None, 
                type = ObjectId(type) if type else None,
                set_name = set_name, 
                set_serialnumber = set_serialnumber if set_serialnumber != float('nan') else None, 
                set_launched = datetime.datetime.strptime(set_launched, TIMESTAMP_PATTERN) if set_launched else None, 
                set_checked = datetime.datetime.strptime(set_checked, TIMESTAMP_PATTERN) if set_checked else None, 
                set_state = ObjectId(set_state) if set_state else None, set_supervisor = ObjectId(set_supervisor) if set_supervisor else None, 
                set_type = ObjectId(set_type) if set_type else None
            )]
            ok = True
        except IndexError:
            ok = False
        return UpdateSystems(systems = systems, ok = ok)