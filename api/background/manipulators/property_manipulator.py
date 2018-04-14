import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from property_mapper import PropertyMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateProperty(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        type = graphene.String()
        admission = graphene.String()
        comissioning = graphene.String()
        department = graphene.String()

    ok = graphene.Boolean()
    property = graphene.Field(lambda: PropertyMapper)

    def mutate(self, info, name, type, admission, comissioning, department):
        property = PropertyMapper.init_scalar(mongo_native.create_property(\
            name, type, datetime.datetime.strptime(admission, TIMESTAMP_PATTERN), datetime.datetime.strptime(comissioning, TIMESTAMP_PATTERN), department\
        ))
        ok = True
        return CreateProperty(property = property, ok = ok)

class RemoveProperty(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    property = graphene.Field(lambda: PropertyMapper)

    def mutate(self, info, id):
        property = PropertyMapper.init_scalar(mongo_native.remove_property(id))
        ok = True
        return RemoveProperty(property = property, ok = ok)