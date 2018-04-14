import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from system_mapper import SystemMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

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
        system = SystemMapper.init_scalar(mongo_native.create_system(\
            name, serialnumber, datetime.datetime.strptime(launched, TIMESTAMP_PATTERN), datetime.datetime.strptime(checked, TIMESTAMP_PATTERN), state, supervisor, type\
        ))
        ok = True
        return CreateSystem(system = system, ok = ok)

class RemoveSystem(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    system = graphene.Field(lambda: SystemMapper)

    def mutate(self, info, id):
        system = SystemMapper.init_scalar(mongo_native.remove_system(id))
        ok = True
        return RemoveSystem(system = system, ok = ok)