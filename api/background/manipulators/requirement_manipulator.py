import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from requirement_mapper import RequirementMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations')

import neo4j_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateRequirement(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        content = graphene.String()

    ok = graphene.Boolean()
    requirement = graphene.Field(lambda: RequirementMapper)

    def mutate(self, info, name, content):
        requirement = RequirementMapper.init_scalar(neo4j_mediator.create_requirement(name, content))
        ok = True
        return CreateRequirement(requirement = requirement, ok = ok)

class RemoveRequirement(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    requirement = graphene.Field(lambda: RequirementMapper)

    def mutate(self, info, id):
        requirement = RequirementMapper.init_scalar(neo4j_mediator.remove_requirement(id))
        ok = True
        return RemoveRequirement(requirement = requirement, ok = ok)

class UpdateRequirements(graphene.Mutation):
    class Arguments:
        name = graphene.String(default_value = '')
        specializations = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_excesses = graphene.String(default_value = '')
        set_expansions = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, name, specializations, set_name, set_excesses, set_expansions):
        neo4j_mediator.update_requirements(name = name, specializations = specializations, set_name = set_name, expansions = set_expansions, excesses = set_excesses)
        ok = True
        return UpdateRequirements(ok = ok)