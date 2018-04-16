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
import sensor_manipulator
import department_manipulator
import person_manipulator
import specialization_manipulator
import boat_manipulator
import system_type_manipulator
import system_state_manipulator
import property_type_manipulator
import system_manipulator
import property_manipulator

import shift_manipulator
import operation_manipulator
import requirement_manipulator

import position_manipulator
import control_action_manipulator
import system_test_manipulator
import sensor_data_manipulator
import shift_state_manipulator
import operation_state_manipulator

def has_item_valid_time(hour, minute, second, item_time):
    return (hour < 0 or item_time.hour == hour) and\
        (minute < 0 or item_time.minute == minute) and\
        (second < 0 or item_time.second == second)

class FirstMutation(graphene.ObjectType):
    create_location = location_manipulator.CreateLocation.Field()
    remove_location = location_manipulator.RemoveLocation.Field()
    eradicate_location = location_manipulator.EradicateLocation.Field()

    create_sensor = sensor_manipulator.CreateSensor.Field()
    remove_sensor = sensor_manipulator.RemoveSensor.Field()
    update_sensors = sensor_manipulator.UpdateSensors.Field()

    create_department = department_manipulator.CreateDepartment.Field()
    remove_department = department_manipulator.RemoveDepartment.Field()
    eradicate_department = department_manipulator.EradicateDepartment.Field()

    create_specialization = specialization_manipulator.CreateSpecialization.Field()
    remove_specialization = specialization_manipulator.RemoveSpecialization.Field()
    eradicate_specialization = specialization_manipulator.Eradicate.Field()

    create_person = person_manipulator.CreatePerson.Field()
    remove_person = person_manipulator.RemovePerson.Field()
    eradicate_person = person_manipulator.EradicatePerson.Field()

    create_boat = boat_manipulator.CreateBoat.Field()
    remove_boat = boat_manipulator.RemoveBoat.Field()

    create_systemtype = system_type_manipulator.CreateSystemType.Field()
    remove_systemtype = system_type_manipulator.RemoveSystemType.Field()
    eradicate_systemtype = system_type_manipulator.EradicateSystemType.Field()

    create_systemstate = system_state_manipulator.CreateSystemState.Field()
    remove_systemstate = system_state_manipulator.RemoveSystemState.Field()
    eradicate_systemstate = system_state_manipulator.EradicateSystemState.Field()

    create_propertytype = property_type_manipulator.CreatePropertyType.Field()
    remove_propertytype = property_type_manipulator.RemovePropertyType.Field()
    eradicate_propertytype = property_type_manipulator.EradicatePropertyType.Field()

    create_system = system_manipulator.CreateSystem.Field()
    remove_system = system_manipulator.RemoveSystem.Field()

    create_property = property_manipulator.CreateProperty.Field()
    remove_property = property_manipulator.RemoveProperty.Field()

    #

    create_shift = shift_manipulator.CreateShift.Field()
    remove_shift = shift_manipulator.RemoveShift.Field()

    create_operation = operation_manipulator.CreateOperation.Field()
    remove_operation = operation_manipulator.RemoveOperation.Field()

    create_requirement = requirement_manipulator.CreateRequirement.Field()
    remove_requirement = requirement_manipulator.RemoveRequirement.Field()

    #

    create_position = position_manipulator.CreatePosition.Field()
    remove_position = position_manipulator.RemovePosition.Field()

    create_controlaction = control_action_manipulator.CreateControlAction.Field()
    remove_controlaction = control_action_manipulator.RemoveControlAction.Field()

    create_systemtest = system_test_manipulator.CreateSystemTest.Field()
    remove_systemtest = system_test_manipulator.RemoveSystemTest.Field()

    create_sensordata = sensor_data_manipulator.CreateSensorData.Field()
    remove_sensordata = sensor_data_manipulator.RemoveSensorData.Field()

    create_shiftstate = shift_state_manipulator.CreateShiftState.Field()
    remove_shiftstate = shift_state_manipulator.RemoveShiftState.Field()

    create_operationstate = operation_state_manipulator.CreateOperationState.Field()
    remove_operationstate = operation_state_manipulator.RemoveOperationState.Field()

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

def get_mutation_description(explored_class):
    result = str(explored_class).lower().replace('create','create_').replace('remove','remove_').replace('eradicate','eradicate_') + ' {\n'
    for field in dir(explored_class.Arguments()):
        if '__' not in field:
            try:
                result += ('    ' + field + ': ' + str(type(getattr(explored_class.Arguments(),field))) + '\n')
            except:
                result += ('    ' + field + '\n')
    result += '}\n\n'
    return result

def get_docs():
    result = ''
    result += get_mutation_description(location_manipulator.CreateLocation)
    result += get_mutation_description(location_manipulator.RemoveLocation)
    result += get_mutation_description(location_manipulator.EradicateLocation)
    result += get_mutation_description(sensor_manipulator.CreateSensor)
    result += get_mutation_description(sensor_manipulator.RemoveSensor)
    result += get_mutation_description(department_manipulator.CreateDepartment)
    result += get_mutation_description(department_manipulator.RemoveDepartment)
    result += get_mutation_description(department_manipulator.EradicateDepartment)
    result += get_mutation_description(specialization_manipulator.CreateSpecialization)
    result += get_mutation_description(specialization_manipulator.RemoveSpecialization)
    result += get_mutation_description(specialization_manipulator.Eradicate)
    result += get_mutation_description(person_manipulator.CreatePerson)
    result += get_mutation_description(person_manipulator.RemovePerson)
    result += get_mutation_description(person_manipulator.EradicatePerson)
    result += get_mutation_description(boat_manipulator.CreateBoat)
    result += get_mutation_description(boat_manipulator.RemoveBoat)
    result += get_mutation_description(system_type_manipulator.CreateSystemType)
    result += get_mutation_description(system_type_manipulator.RemoveSystemType)
    result += get_mutation_description(system_type_manipulator.EradicateSystemType)
    result += get_mutation_description(system_state_manipulator.CreateSystemState)
    result += get_mutation_description(system_state_manipulator.RemoveSystemState)
    result += get_mutation_description(system_state_manipulator.EradicateSystemState)
    result += get_mutation_description(property_type_manipulator.CreatePropertyType)
    result += get_mutation_description(property_type_manipulator.RemovePropertyType)
    result += get_mutation_description(property_type_manipulator.EradicatePropertyType)
    result += get_mutation_description(system_manipulator.CreateSystem)
    result += get_mutation_description(system_manipulator.RemoveSystem)
    result += get_mutation_description(property_manipulator.CreateProperty)
    result += get_mutation_description(property_manipulator.RemoveProperty)
    result += get_mutation_description(shift_manipulator.CreateShift)
    result += get_mutation_description(shift_manipulator.RemoveShift)
    result += get_mutation_description(operation_manipulator.CreateOperation)
    result += get_mutation_description(operation_manipulator.RemoveOperation)
    result += get_mutation_description(requirement_manipulator.CreateRequirement)
    result += get_mutation_description(requirement_manipulator.RemoveRequirement)
    result += get_mutation_description(position_manipulator.CreatePosition)
    result += get_mutation_description(position_manipulator.RemovePosition)
    result += get_mutation_description(control_action_manipulator.CreateControlAction)
    result += get_mutation_description(control_action_manipulator.RemoveControlAction)
    result += get_mutation_description(system_test_manipulator.CreateSystemTest)
    result += get_mutation_description(system_test_manipulator.RemoveSystemTest)
    result += get_mutation_description(sensor_data_manipulator.CreateSensorData)
    result += get_mutation_description(sensor_data_manipulator.RemoveSensorData)
    result += get_mutation_description(shift_state_manipulator.CreateShiftState)
    result += get_mutation_description(shift_state_manipulator.RemoveShiftState)
    result += get_mutation_description(operation_state_manipulator.CreateOperationState)
    result += get_mutation_description(operation_state_manipulator.RemoveOperationState)

    return result

def main():
    if len(sys.argv) < 2:
        print('There is no query')
        sys.exit()

    query = sys.argv[1]

    if query == 'docs':
        print(get_docs())
        print('=====')
        return
    
    connection.setup([DB_URL], DB_NAME)
    schema = graphene.Schema(query = FirstQuery, mutation = FirstMutation)
     
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


if __name__ == '__main__':
    main()