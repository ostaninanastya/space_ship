import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from operation_mapper import OperationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations')

import neo4j_mediator

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
        operation = OperationMapper.init_scalar(neo4j_mediator.create_operation(\
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
        operation = OperationMapper.init_scalar(neo4j_mediator.remove_operation(id))
        ok = True
        return RemoveOperation(operation = operation, ok = ok)