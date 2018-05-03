import sys, os, re
import graphene

from specialization_mapper import SpecializationMapper
from department_mapper import DepartmentMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/lobgook/native')

#import select_queries

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/')

import cassandra_mediator

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import neo4j_mediator

class PersonMapper(graphene.ObjectType):
    id = graphene.String()

    name = graphene.String(default_value = '')
    surname = graphene.String(default_value = '')
    patronymic = graphene.String(default_value = '')
    phone = graphene.String(default_value = '')
    department = graphene.Field(lambda: DepartmentMapper)
    directing = graphene.List(lambda: DepartmentMapper)
    chiefed = graphene.List('shift_mapper.ShiftMapper')
    worked = graphene.List('shift_mapper.ShiftMapper')
    headed = graphene.List('operation_mapper.OperationMapper')
    executed = graphene.List('operation_mapper.OperationMapper')
    specialization = graphene.Field(lambda: SpecializationMapper)
    commands = graphene.List('control_action_mapper.ControlActionMapper')
    supervised = graphene.List('system_mapper.SystemMapper')

    def resolve_supervised(self, info):
        from system_mapper import SystemMapper
        return [SystemMapper.init_scalar(item) for item in mongo_mediator.get_systems_by_supervisor_id(self.id)]

    def resolve_directing(self, info):
        return [DepartmentMapper.init_scalar(mongo_mediator.get_department_by_id(deparment_id)) for deparment_id in neo4j_adapter.get_directed_ids(self.id)]

    def resolve_department(self, info):
        return DepartmentMapper.init_scalar(mongo_mediator.get_department_by_id(self.department))
    
    def resolve_chiefed(self, info):
        from shift_mapper import ShiftMapper
        return [ShiftMapper.init_scalar(item) for item in neo4j_mediator.get_chiefed_shifts(self.id)]

    def resolve_worked(self, info):
        from shift_mapper import ShiftMapper
        return [ShiftMapper.init_scalar(item) for item in neo4j_mediator.get_worked_shifts(self.id)]

    def resolve_headed(self, info):
        from operation_mapper import OperationMapper
        return [OperationMapper.init_scalar(item) for item in neo4j_mediator.get_headed_operations(self.id)]

    def resolve_executed(self, info):
        from operation_mapper import OperationMapper
        return [OperationMapper.init_scalar(item) for item in neo4j_mediator.get_executed_operations(self.id)]

    def resolve_specialization(self, info):
        return SpecializationMapper.init_scalar(mongo_mediator.get_specialization_by_id(self.specialization))

    def resolve_commands(self, info):
        from control_action_mapper import ControlActionMapper
        return [ControlActionMapper.init_scalar_dict(item) for item in cassandra_mediator.get_commands_by_user_id(self.id)]

    @staticmethod
    def eject(id, name, surname, patronymic, phone, department, specialization):
        return [PersonMapper.init_scalar(item)\
            for item in mongo_mediator.select_people(name = name, surname = surname, patronymic = patronymic, phone = phone, 
                ids = {'_id': id, 'department': department, 'specialization': specialization})]

    @staticmethod
    def init_scalar(item):
        return PersonMapper(id = str(item['_id']), name = item['name'], surname = item.get('surname'), 
            patronymic = item.get('patronymic'), phone = item.get('phone'))


