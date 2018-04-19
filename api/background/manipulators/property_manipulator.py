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

class UpdateProperties(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        type = graphene.String(default_value = '')
        admission = graphene.String(default_value = '')
        comissioning = graphene.String(default_value = '')
        department = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_type = graphene.String(default_value = '')
        set_admission = graphene.String(default_value = '')
        set_comissioning = graphene.String(default_value = '')
        set_department = graphene.String(default_value = '')

    ok = graphene.Boolean()
    properties = graphene.List(lambda: PropertyMapper)

    def mutate(self, info, id, name, type, admission, comissioning, department, set_name, set_type, set_admission, set_comissioning, set_department):
        properties = [PropertyMapper.init_scalar(item) for item in mongo_native.update_properties(\
            _id = ObjectId(id) if id else None, name = name, type = ObjectId(type) if type else None, 
            admission = datetime.datetime.strptime(admission, TIMESTAMP_PATTERN) if admission else None, 
            comissioning = datetime.datetime.strptime(comissioning, TIMESTAMP_PATTERN) if comissioning else None, 
            department = ObjectId(department) if department else None,
            set_name = set_name, set_type = ObjectId(set_type) if set_type else None, 
            set_admission = datetime.datetime.strptime(set_admission, TIMESTAMP_PATTERN) if set_admission else None, 
            set_comissioning = datetime.datetime.strptime(set_comissioning, TIMESTAMP_PATTERN) if set_comissioning else None, 
            set_department = ObjectId(set_department) if set_department else None
        )]
        ok = True
        return UpdateProperties(properties = properties, ok = ok)