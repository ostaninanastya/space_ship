import sys, os, re
import configparser
import datetime
import json

config = configparser.ConfigParser()
config.read('../../databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host']
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

import graphene
from cassandra.cqlengine import connection

sys.path.append('../../logbook/entities')

from position import Position
from control_action import ControlAction

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter
import neo4j_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/native/')

import select_queries

from converters import time_to_str, date_to_str

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/entities/')

from requirement import Requirement
from shift import Shift
from operation import Operation

from control_action_mapper import ControlActionMapper
from position_mapper import PositionMapper
from system_test_mapper import SystemTestMapper
from operation_state_mapper import OperationStateMapper
from shift_state_mapper import ShiftStateMapper
from sensor_data_mapper import SensorDataMapper

from person_mapper import PersonMapper
from department_mapper import DepartmentMapper
from property_type_mapper import PropertyTypeMapper
from specialization_mapper import SpecializationMapper
from property_mapper import PropertyMapper
from system_state_mapper import SystemStateMapper
from system_type_mapper import SystemTypeMapper
from location_mapper import LocationMapper
from boat_mapper import BoatMapper
from sensor_mapper import SensorMapper
from system_mapper import SystemMapper

from requirement_mapper import RequirementMapper
from shift_mapper import ShiftMapper
from operation_mapper import OperationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/native')

import mongo_native

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/manipulators')

import location_manipulator

def has_item_valid_time(hour, minute, second, item_time):
    return (hour < 0 or item_time.hour == hour) and\
        (minute < 0 or item_time.minute == minute) and\
        (second < 0 or item_time.second == second)

class FirstMutation(graphene.ObjectType):
    create_location = location_manipulator.CreateLocation.Field()
    remove_location = location_manipulator.RemoveLocation.Field()

class FirstQuery(graphene.ObjectType):

    position = graphene.List(PositionMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    controlaction = graphene.List(ControlActionMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    systemtest = graphene.List(SystemTestMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    operationstate = graphene.List(OperationStateMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    shiftstate = graphene.List(ShiftStateMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))
    sensordata = graphene.List(SensorDataMapper, hour = graphene.Int(default_value = -1), minute = graphene.Int(default_value = -1), second = graphene.Int(default_value = -1))

    people = graphene.List(PersonMapper, id = graphene.String(default_value = ''))
    departments = graphene.List(DepartmentMapper, id = graphene.String(default_value = ''))
    property_types = graphene.List(PropertyTypeMapper, id = graphene.String(default_value = ''))
    specializations = graphene.List(SpecializationMapper, id = graphene.String(default_value = ''))
    properties = graphene.List(PropertyMapper, id = graphene.String(default_value = ''))
    systemstates = graphene.List(SystemStateMapper, id = graphene.String(default_value = ''))
    systemtypes = graphene.List(SystemTypeMapper, id = graphene.String(default_value = ''))
    locations = graphene.List(LocationMapper, id = graphene.String(default_value = ''))
    boats = graphene.List(BoatMapper, id = graphene.String(default_value = ''))
    sensors = graphene.List(SensorMapper, id = graphene.String(default_value = ''))
    systems = graphene.List(SystemMapper, id = graphene.String(default_value = ''))

    requirements = graphene.List(RequirementMapper, id = graphene.String(default_value = ''))
    shifts = graphene.List(ShiftMapper, id = graphene.String(default_value = ''))
    operations = graphene.List(OperationMapper, id = graphene.String(default_value = ''))

    #recital

    def resolve_people(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [PersonMapper(person_id) for person_id in mongo_native.get_all_people_ids() if id_matcher.match(person_id)]

    def resolve_departments(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [DepartmentMapper(department_id) for department_id in mongo_native.get_all_departments_ids() if id_matcher.match(department_id)]

    def resolve_property_types(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [PropertyTypeMapper.init_scalar(item) for item in mongo_native.get_all_property_types() if id_matcher.match(str(item['_id']))]

    def resolve_specializations(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [SpecializationMapper(spec_id) for spec_id in mongo_native.get_all_specializations_ids() if id_matcher.match(spec_id)]

    def resolve_properties(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [PropertyMapper.init_scalar(item) for item in mongo_native.get_all_properties() if id_matcher.match(str(item['_id']))]

    def resolve_systemstates(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [SystemStateMapper.init_scalar(item) for item in mongo_native.get_all_system_states() if id_matcher.match(str(item['_id']))]

    def resolve_systemtypes(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [SystemTypeMapper.init_scalar(item) for item in mongo_native.get_all_system_types() if id_matcher.match(str(item['_id']))]

    def resolve_locations(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [LocationMapper.init_scalar(item) for item in mongo_native.get_all_locations() if id_matcher.match(str(item['_id']))]

    def resolve_boats(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [BoatMapper.init_scalar(item) for item in mongo_native.get_all_boats() if id_matcher.match(str(item['_id']))]

    def resolve_sensors(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [SensorMapper.init_scalar(item) for item in mongo_native.get_all_sensors() if id_matcher.match(str(item['_id']))]

    def resolve_systems(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [SystemMapper.init_scalar(item) for item in mongo_native.get_all_systems() if id_matcher.match(str(item['_id']))]

    #logbook

    def resolve_systemtest(self, info, hour, minute, second):
        return [SystemTestMapper.init_scalar(item) for item in select_queries.get_system_tests() 
        if has_item_valid_time(hour, minute, second, item['time'])]

    def resolve_controlaction(self, info, hour, minute, second):
        return [ControlActionMapper.init_scalar(item) for item in ControlAction.objects.all()[1:] 
        if has_item_valid_time(hour, minute, second, item.time)]

    def resolve_position(self, info, hour, minute, second):
        return [PositionMapper.init_scalar(item) for item in Position.objects.all()[1:] 
        if has_item_valid_time(hour, minute, second, item.time)]

    def resolve_operationstate(self, info, hour, minute, second):
        return [OperationStateMapper.init_scalar(item) for item in select_queries.get_operation_states()
        if has_item_valid_time(hour, minute, second, item['time'])]

    def resolve_shiftstate(self, info, hour, minute, second):
        return [ShiftStateMapper.init_scalar(item) for item in select_queries.get_shift_states() 
        if has_item_valid_time(hour, minute, second, item['time'])]

    def resolve_sensordata(self, info, hour, minute, second):
        return [SensorDataMapper.init_scalar(item) for item in select_queries.get_sensor_data() 
        if has_item_valid_time(hour, minute, second, item['time'])]

    #relations

    def resolve_requirements(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [RequirementMapper.init_scalar(item) for item in Requirement.nodes.filter() if id_matcher.match(str(item.ident))]

    def resolve_shifts(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [ShiftMapper.init_scalar(item) for item in Shift.nodes.filter() if id_matcher.match(str(item.ident))]

    def resolve_operations(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [OperationMapper.init_scalar(item) for item in Operation.nodes.filter() if id_matcher.match(str(item.ident))]


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print('There is no query')
        sys.exit()
    
    connection.setup([DB_URL], DB_NAME)
    schema = graphene.Schema(query = FirstQuery, mutation = FirstMutation)
    query = sys.argv[1] 
    '''
        query MyFirstQuery {
          position(hour : 20, second : 12){
            x,
            y,
            speed,
            time,
            date
          }
        }
    '''
    print(json.dumps(schema.execute(query).data, indent = 4, sort_keys = True))
    print('=====')