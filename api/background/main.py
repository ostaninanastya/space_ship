import sys, os, re
import configparser
import datetime
import json

config = configparser.ConfigParser()
config.read('../../databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host']
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

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

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import string_to_bytes

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

INFINITY = float('inf')

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations')

import neo4j_mediator

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
    update_departments = department_manipulator.UpdateDepartments.Field()

    create_specialization = specialization_manipulator.CreateSpecialization.Field()
    remove_specialization = specialization_manipulator.RemoveSpecialization.Field()
    eradicate_specialization = specialization_manipulator.Eradicate.Field()

    create_person = person_manipulator.CreatePerson.Field()
    remove_person = person_manipulator.RemovePerson.Field()
    eradicate_person = person_manipulator.EradicatePerson.Field()
    update_people = person_manipulator.UpdatePeople.Field()

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
    update_position = position_manipulator.UpdatePositions.Field()

    create_controlaction = control_action_manipulator.CreateControlAction.Field()
    remove_controlaction = control_action_manipulator.RemoveControlAction.Field()
    update_controlaction = control_action_manipulator.UpdateControlActions.Field()

    create_systemtest = system_test_manipulator.CreateSystemTest.Field()
    remove_systemtest = system_test_manipulator.RemoveSystemTest.Field()
    update_systemtest = system_test_manipulator.UpdateSystemTests.Field()

    create_sensordata = sensor_data_manipulator.CreateSensorData.Field()
    remove_sensordata = sensor_data_manipulator.RemoveSensorData.Field()
    update_sensordata = sensor_data_manipulator.UpdateSensorData.Field()

    create_shiftstate = shift_state_manipulator.CreateShiftState.Field()
    remove_shiftstate = shift_state_manipulator.RemoveShiftState.Field()
    update_shiftstate = shift_state_manipulator.UpdateShiftStates.Field()

    create_operationstate = operation_state_manipulator.CreateOperationState.Field()
    remove_operationstate = operation_state_manipulator.RemoveOperationState.Field()
    update_operationstate = operation_state_manipulator.UpdateOperationStates.Field()

class FirstQuery(graphene.ObjectType):

    position = graphene.List(PositionMapper, date = graphene.String(default_value = ''),
        time = graphene.String(default_value = ''),
        x = graphene.Float(default_value = float('nan')),
        y = graphene.Float(default_value = float('nan')),
        z = graphene.Float(default_value = float('nan')),
        attack_angle = graphene.Float(default_value = float('nan')),
        direction_angle = graphene.Float(default_value = float('nan')),
        speed = graphene.Float(default_value = float('nan')))
    controlaction = graphene.List(ControlActionMapper, date = graphene.String(default_value = ''),
        time = graphene.String(default_value = ''),
        mac = graphene.String(default_value = ''),
        user = graphene.String(default_value = ''),
        command = graphene.String(default_value = ''),
        params = graphene.String(default_value = ''),
        result = graphene.String(default_value = ''))
    systemtest = graphene.List(SystemTestMapper, date = graphene.String(default_value = ''),
        time = graphene.String(default_value = ''),
        system = graphene.String(default_value = ''),
        result = graphene.Int(default_value = -1))
    operationstate = graphene.List(OperationStateMapper,date = graphene.String(default_value = ''),
        time = graphene.String(default_value = ''),
        boat = graphene.String(default_value = ''),
        operation = graphene.String(default_value = ''),
        status = graphene.String(default_value = ''),
        distancetotheship = graphene.Float(default_value = float('nan')),
        zenith = graphene.Float(default_value = float('nan')),
        azimuth = graphene.Float(default_value = float('nan')),
        hydrogenium = graphene.Float(default_value = float('nan')),
        helium = graphene.Float(default_value = float('nan')),
        lithium = graphene.Float(default_value = float('nan')),
        beryllium = graphene.Float(default_value = float('nan')),
        borum = graphene.Float(default_value = float('nan')),
        carboneum = graphene.Float(default_value = float('nan')),
        nitrogenium = graphene.Float(default_value = float('nan')),
        oxygenium = graphene.Float(default_value = float('nan')),
        fluorum = graphene.Float(default_value = float('nan')),
        neon = graphene.Float(default_value = float('nan')),
        natrium = graphene.Float(default_value = float('nan')),
        magnesium = graphene.Float(default_value = float('nan')),
        aluminium = graphene.Float(default_value = float('nan')),
        silicium = graphene.Float(default_value = float('nan')),
        phosphorus = graphene.Float(default_value = float('nan')),
        sulfur = graphene.Float(default_value = float('nan')),
        chlorum = graphene.Float(default_value = float('nan')),
        argon = graphene.Float(default_value = float('nan')),
        kalium = graphene.Float(default_value = float('nan')),
        calcium = graphene.Float(default_value = float('nan')),
        scandium = graphene.Float(default_value = float('nan')),
        titanium = graphene.Float(default_value = float('nan')),
        vanadium = graphene.Float(default_value = float('nan')),
        chromium = graphene.Float(default_value = float('nan')),
        manganum  = graphene.Float(default_value = float('nan')),
        ferrum = graphene.Float(default_value = float('nan')),
        cobaltum = graphene.Float(default_value = float('nan')),
        niccolum = graphene.Float(default_value = float('nan')),
        cuprum = graphene.Float(default_value = float('nan')),
        zincum = graphene.Float(default_value = float('nan')),
        gallium = graphene.Float(default_value = float('nan')),
        germanium = graphene.Float(default_value = float('nan')),
        arsenicum = graphene.Float(default_value = float('nan')),
        selenium = graphene.Float(default_value = float('nan')),
        bromum = graphene.Float(default_value = float('nan')),
        crypton = graphene.Float(default_value = float('nan')),
        rubidium = graphene.Float(default_value = float('nan')),
        strontium = graphene.Float(default_value = float('nan')),
        yttrium = graphene.Float(default_value = float('nan')),
        zirconium = graphene.Float(default_value = float('nan')),
        niobium = graphene.Float(default_value = float('nan')),
        molybdaenum = graphene.Float(default_value = float('nan')),
        technetium = graphene.Float(default_value = float('nan')),
        ruthenium = graphene.Float(default_value = float('nan')),
        rhodium = graphene.Float(default_value = float('nan')),
        palladium = graphene.Float(default_value = float('nan')),
        argentum = graphene.Float(default_value = float('nan')),
        cadmium = graphene.Float(default_value = float('nan')),
        indium = graphene.Float(default_value = float('nan')),
        stannum = graphene.Float(default_value = float('nan')),
        stibium = graphene.Float(default_value = float('nan')),
        tellurium = graphene.Float(default_value = float('nan')),
        iodium = graphene.Float(default_value = float('nan')),
        xenon = graphene.Float(default_value = float('nan')),
        caesium = graphene.Float(default_value = float('nan')),
        barium = graphene.Float(default_value = float('nan')),
        lanthanum = graphene.Float(default_value = float('nan')),
        cerium = graphene.Float(default_value = float('nan')),
        praseodymium = graphene.Float(default_value = float('nan')),
        neodymium = graphene.Float(default_value = float('nan')),
        promethium = graphene.Float(default_value = float('nan')),
        samarium = graphene.Float(default_value = float('nan')),
        europium = graphene.Float(default_value = float('nan')),
        gadolinium = graphene.Float(default_value = float('nan')),
        terbium = graphene.Float(default_value = float('nan')),
        dysprosium = graphene.Float(default_value = float('nan')),
        holmium = graphene.Float(default_value = float('nan')),
        erbium = graphene.Float(default_value = float('nan')),
        thulium = graphene.Float(default_value = float('nan')),
        ytterbium = graphene.Float(default_value = float('nan')),
        lutetium = graphene.Float(default_value = float('nan')),
        hafnium = graphene.Float(default_value = float('nan')),
        tantalum = graphene.Float(default_value = float('nan')),
        wolframium = graphene.Float(default_value = float('nan')),
        rhenium = graphene.Float(default_value = float('nan')),
        osmium = graphene.Float(default_value = float('nan')),
        iridium = graphene.Float(default_value = float('nan')),
        platinum = graphene.Float(default_value = float('nan')),
        aurum = graphene.Float(default_value = float('nan')),
        hydrargyrum = graphene.Float(default_value = float('nan')),
        thallium = graphene.Float(default_value = float('nan')),
        plumbum = graphene.Float(default_value = float('nan')),
        bismuthum = graphene.Float(default_value = float('nan')),
        polonium = graphene.Float(default_value = float('nan')),
        astatum = graphene.Float(default_value = float('nan')),
        radon = graphene.Float(default_value = float('nan')),
        francium = graphene.Float(default_value = float('nan')),
        radium = graphene.Float(default_value = float('nan')),
        actinium = graphene.Float(default_value = float('nan')),
        thorium = graphene.Float(default_value = float('nan')),
        protactinium = graphene.Float(default_value = float('nan')),
        uranium = graphene.Float(default_value = float('nan')),
        neptunium = graphene.Float(default_value = float('nan')),
        plutonium = graphene.Float(default_value = float('nan')),
        americium = graphene.Float(default_value = float('nan')),
        curium = graphene.Float(default_value = float('nan')),
        berkelium = graphene.Float(default_value = float('nan')),
        californium = graphene.Float(default_value = float('nan')),
        einsteinium = graphene.Float(default_value = float('nan')),
        fermium = graphene.Float(default_value = float('nan')),
        mendelevium  = graphene.Float(default_value = float('nan')),
        nobelium = graphene.Float(default_value = float('nan')),
        lawrencium  = graphene.Float(default_value = float('nan')),
        rutherfordium = graphene.Float(default_value = float('nan')),
        dubnium = graphene.Float(default_value = float('nan')),
        seaborgium = graphene.Float(default_value = float('nan')),
        bohrium = graphene.Float(default_value = float('nan')),
        hassium = graphene.Float(default_value = float('nan')),
        meitnerium = graphene.Float(default_value = float('nan')),
        darmstadtium = graphene.Float(default_value = float('nan')),
        roentgenium = graphene.Float(default_value = float('nan')),
        copernicium = graphene.Float(default_value = float('nan')),
        nihonium = graphene.Float(default_value = float('nan')),
        flerovium = graphene.Float(default_value = float('nan')),
        moscovium = graphene.Float(default_value = float('nan')),
        livermorium = graphene.Float(default_value = float('nan')),
        tennessium = graphene.Float(default_value = float('nan')),
        oganesson = graphene.Float(default_value = float('nan')),
        comment = graphene.String(default_value = ''))
    shiftstate = graphene.List(ShiftStateMapper, date = graphene.String(default_value = ''),
        time = graphene.String(default_value = ''),
        shift = graphene.String(default_value = ''),
        warninglevel = graphene.String(default_value = ''),
        remainingcartridges = graphene.Int(default_value = -1),
        remainingair = graphene.Int(default_value = -1),
        remainingelectricity = graphene.Int(default_value = -1),
        comment = graphene.String(default_value = ''))
    sensordata = graphene.List(SensorDataMapper, date = graphene.String(default_value = ''),
        time = graphene.String(default_value = ''),
        sensor = graphene.String(default_value = ''),
        event = graphene.String(default_value = ''),
        valuename = graphene.String(default_value = ''),
        value = graphene.Float(default_value = float('nan')),
        units = graphene.String(default_value = ''))

    people = graphene.List(PersonMapper, id = graphene.String(default_value = ''),
        name = graphene.String(default_value = ''),
        surname = graphene.String(default_value = ''),
        patronymic = graphene.String(default_value = ''),
        phone = graphene.String(default_value = ''),
        department = graphene.String(default_value = ''),
        specialization = graphene.String(default_value = ''))
    departments = graphene.List(DepartmentMapper, id = graphene.String(default_value = ''),
        name = graphene.String(default_value = ''),
        vk = graphene.String(default_value = ''))
    property_types = graphene.List(PropertyTypeMapper, id = graphene.String(default_value = ''))
    specializations = graphene.List(SpecializationMapper, id = graphene.String(default_value = ''))
    properties = graphene.List(PropertyMapper, id = graphene.String(default_value = ''))
    systemstates = graphene.List(SystemStateMapper, id = graphene.String(default_value = ''))
    systemtypes = graphene.List(SystemTypeMapper, id = graphene.String(default_value = ''))
    locations = graphene.List(LocationMapper, id = graphene.String(default_value = ''))
    boats = graphene.List(BoatMapper, id = graphene.String(default_value = ''))
    sensors = graphene.List(SensorMapper, id = graphene.String(default_value = ''), 
        name = graphene.String(default_value = ''),
        location = graphene.String(default_value = ''))
    systems = graphene.List(SystemMapper, id = graphene.String(default_value = ''))

    requirements = graphene.List(RequirementMapper, id = graphene.String(default_value = ''))
    shifts = graphene.List(ShiftMapper, id = graphene.String(default_value = ''))
    operations = graphene.List(OperationMapper, id = graphene.String(default_value = ''), name = graphene.String(default_value = ''),
        start = graphene.String(default_value = ''), end = graphene.String(default_value = ''))

    #recital

    def resolve_people(self, info, id, name, surname, patronymic, phone, department, specialization):
        id_matcher = re.compile(id + '.*')
        department_id_matcher = re.compile(department + '.*')
        specialization_id_matcher = re.compile(specialization + '.*')
        return [PersonMapper.init_scalar(item)\
        for item in mongo_native.select_people(name = name, surname = surname, patronymic = patronymic, phone = phone)\
        if id_matcher.match(str(item['_id'])) and department_id_matcher.match(str(item['department'])) and specialization_id_matcher.match(str(item['specialization']))]

    def resolve_departments(self, info, id, name, vk):
        id_matcher = re.compile(id + '.*')
        return [DepartmentMapper.init_scalar(item) for item in mongo_native.select_departments(name = name, vk = vk) if id_matcher.match(str(item['_id']))]

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

    def resolve_sensors(self, info, id, name, location):
        id_matcher = re.compile(id + '.*')
        location_id_matcher = re.compile(location + '.*')
        return [SensorMapper.init_scalar(item) for item in mongo_native.select_sensors(name = name)\
            if id_matcher.match(str(item['_id'])) and location_id_matcher.match(str(item.get('location')))]

    def resolve_systems(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [SystemMapper.init_scalar(item) for item in mongo_native.get_all_systems() if id_matcher.match(str(item['_id']))]

    #logbook

    def resolve_systemtest(self, info, date, time, system, result):
        return [SystemTestMapper.init_scalar(item) for item in cassandra_mediator.select_system_tests(
            date = None if not date else datetime.datetime.strptime(date, DATE_PATTERN).date(),
            time = None if not time else datetime.datetime.strptime(time, TIME_PATTERN).time(),
            system_id = None if not system else string_to_bytes(system),
            result = result)]

    def resolve_controlaction(self, info, date, time, mac, user, command, params, result):
        return [ControlActionMapper.init_scalar(item) for item in cassandra_mediator.select_control_actions(
            date = None if not date else datetime.datetime.strptime(date, DATE_PATTERN).date(),
            time = None if not time else datetime.datetime.strptime(time, TIME_PATTERN).time(),
            mac_address = None if not mac else string_to_bytes(mac), 
            user_id = None if not user else string_to_bytes(user), 
            command = command, params = params, result = result)]

    def resolve_position(self, info, date, time, x, y, z, speed, attack_angle, direction_angle):
        return [PositionMapper.init_scalar(item) for item in cassandra_mediator.select_positions(
            date = None if not date else datetime.datetime.strptime(date, DATE_PATTERN).date(),
            time = None if not time else datetime.datetime.strptime(time, TIME_PATTERN).time(),
            x = x, y = y, z = z, speed = speed, attack_angle = attack_angle, direction_angle = direction_angle)]

    def resolve_operationstate(self, info, date, time, boat, operation, status, distancetotheship, zenith, azimuth, hydrogenium,
        helium, lithium, beryllium, borum,
        carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,\
        scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,\
        crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,\
        stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,\
        terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,\
        hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,\
        plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,\
        seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,\
        oganesson, comment):
        return [OperationStateMapper.init_scalar(item) for item in cassandra_mediator.select_operation_states(
            date = None if not date else datetime.datetime.strptime(date, DATE_PATTERN).date(),
            time = None if not time else datetime.datetime.strptime(time, TIME_PATTERN).time(),
            boat_id = None if not boat else string_to_bytes(boat),
            operation_id = None if not operation else string_to_bytes(operation),
            status = status, distance_to_the_ship = distancetotheship, zenith = zenith, azimuth = azimuth, 
            hydrogenium = hydrogenium, helium = helium, lithium = lithium, beryllium = beryllium, borum = borum, carboneum = carboneum, 
            nitrogenium = nitrogenium, oxygenium = oxygenium, fluorum = fluorum, neon = neon, natrium = natrium, magnesium = magnesium, 
            aluminium = aluminium, silicium = silicium, phosphorus = phosphorus, sulfur = sulfur, chlorum = chlorum, argon = argon, kalium = kalium, 
            calcium = calcium, scandium = scandium, titanium = titanium, vanadium = vanadium, chromium = chromium, manganum = manganum, 
            ferrum = ferrum, cobaltum = cobaltum, niccolum = niccolum, cuprum = cuprum, zincum = zincum, gallium = gallium, germanium = germanium, 
            arsenicum = arsenicum, selenium = selenium, bromum = bromum, crypton = crypton, rubidium = rubidium, strontium = strontium, 
            yttrium = yttrium, zirconium = zirconium, niobium = niobium, molybdaenum = molybdaenum, technetium = technetium, ruthenium = ruthenium, 
            rhodium = rhodium, palladium = palladium, argentum = argentum, cadmium = cadmium, indium = indium, stannum = stannum, stibium = stibium, 
            tellurium = tellurium, iodium = iodium, xenon = xenon, caesium = caesium, barium = barium, lanthanum = lanthanum, cerium = cerium, 
            praseodymium = praseodymium, neodymium = neodymium, promethium = promethium, samarium = samarium, europium = europium, gadolinium = gadolinium, 
            terbium = terbium, dysprosium = dysprosium, holmium = holmium, erbium = erbium, thulium = thulium, ytterbium = ytterbium, lutetium = lutetium, 
            hafnium = hafnium, tantalum = tantalum, wolframium = wolframium, rhenium = rhenium, osmium = osmium, iridium = iridium, platinum = platinum, 
            aurum = aurum, hydrargyrum = hydrargyrum, thallium = thallium, plumbum = plumbum, bismuthum = bismuthum, polonium = polonium, astatum = astatum, 
            radon = radon, francium = francium, radium = radium, actinium = actinium, thorium = thorium, protactinium = protactinium, uranium = uranium, 
            neptunium = neptunium, plutonium = plutonium, americium = americium, curium = curium, berkelium = berkelium, californium = californium, 
            einsteinium = einsteinium, fermium = fermium, mendelevium = mendelevium, nobelium = nobelium, lawrencium = lawrencium, 
            rutherfordium = rutherfordium, dubnium = dubnium, seaborgium = seaborgium, bohrium = bohrium, hassium = hassium, meitnerium = meitnerium, 
            darmstadtium = darmstadtium, roentgenium = roentgenium, copernicium = copernicium, nihonium = nihonium, flerovium = flerovium, 
            moscovium = moscovium, livermorium = livermorium, tennessium = tennessium, oganesson = oganesson, comment = comment)]

    def resolve_shiftstate(self, info, date, time, shift, warninglevel, remainingcartridges, remainingair, remainingelectricity, comment):
        return [ShiftStateMapper.init_scalar(item) for item in cassandra_mediator.select_shift_states(
            date = None if not date else datetime.datetime.strptime(date, DATE_PATTERN).date(),
            time = None if not time else datetime.datetime.strptime(time, TIME_PATTERN).time(),
            shift_id = None if not shift else string_to_bytes(shift), 
            warning_level = warninglevel, remaining_cartridges = remainingcartridges, remaining_air = remainingair, remaining_electricity = remainingelectricity,
            comment = comment)]

    def resolve_sensordata(self, info, date, time, sensor, event, valuename, value, units):
        return [SensorDataMapper.init_scalar(item) for item in cassandra_mediator.select_sensor_data(
            date = None if not date else datetime.datetime.strptime(date, DATE_PATTERN).date(),
            time = None if not time else datetime.datetime.strptime(time, TIME_PATTERN).time(),
            source_id = None if not sensor else string_to_bytes(sensor), 
            event = event, value_name = valuename, value = value, units = units)]

    #relations

    def resolve_requirements(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [RequirementMapper.init_scalar(item) for item in Requirement.nodes.filter() if id_matcher.match(str(item.ident))]

    def resolve_shifts(self, info, id):
        id_matcher = re.compile(id + '.*')
        return [ShiftMapper.init_scalar(item) for item in Shift.nodes.filter() if id_matcher.match(str(item.ident))]

    def resolve_operations(self, info, id, name, start, end):
        id_matcher = re.compile(id + '.*')

        return [OperationMapper.init_scalar(item) for item in neo4j_mediator.select_operations(name__regex = '.*' + name + '.*',
            start = datetime.datetime.strptime(start, TIMESTAMP_PATTERN) if start else None,
            end = datetime.datetime.strptime(end, TIMESTAMP_PATTERN) if end else None) 
            if id_matcher.match(str(item.ident))]

        #return [OperationMapper.init_scalar(item) for item in Operation.nodes.filter() if id_matcher.match(str(item.ident))]

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