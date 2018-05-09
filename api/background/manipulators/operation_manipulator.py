import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from operation_mapper import OperationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateOperation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        start = graphene.String()
        end = graphene.String()
        head = graphene.String()
        executors = graphene.String()
        requirements = graphene.String()

    ok = graphene.Boolean()
    operation = graphene.Field(lambda: OperationMapper)

    def mutate(self, info, name, head, start, end, executors, requirements):
        operation = OperationMapper.init_scalar(mongo_mediator.create_operation(\
            name, head, datetime.datetime.strptime(start, TIMESTAMP_PATTERN), datetime.datetime.strptime(end, TIMESTAMP_PATTERN), executors, requirements\
        ))
        ok = True
        return CreateOperation(operation = operation, ok = ok)

class RemoveOperation(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    operation = graphene.Field(lambda: OperationMapper)

    def mutate(self, info, id):
        operation = OperationMapper.init_scalar(mongo_mediator.remove_operation(id))
        ok = True
        return RemoveOperation(operation = operation, ok = ok)

class UpdateOperations(graphene.Mutation):
    class Arguments:
        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')
        start = graphene.String(default_value = '')
        end = graphene.String(default_value = '')
        head = graphene.String(default_value = '')
        executors = graphene.String(default_value = '')
        requirements = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_start = graphene.String(default_value = '')
        set_end = graphene.String(default_value = '')
        set_head = graphene.String(default_value = '')
        set_executors = graphene.String(default_value = '')
        set_requirements = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, id, name, head, start, end, executors, requirements, set_name, set_head, set_start, set_end, set_executors, set_requirements):
        mongo_mediator.update_operations(ident = id,
            name = name, head = head,
            start = None if not start else datetime.datetime.strptime(start, TIMESTAMP_PATTERN), 
            end = None if not end else datetime.datetime.strptime(end, TIMESTAMP_PATTERN), 
            executors = executors, requirements = requirements,
            set_name = set_name, set_head = set_head, set_start = None if not set_start else datetime.datetime.strptime(set_start, TIMESTAMP_PATTERN), 
            set_end = None if not set_end else datetime.datetime.strptime(set_end, TIMESTAMP_PATTERN), set_executors = set_executors, 
            set_requirements = set_requirements
        )
        ok = True
        return UpdateOperations(ok = ok)