import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

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

from control_action_mapper import ControlActionMapper
from position_mapper import PositionMapper
from system_test_mapper import SystemTestMapper
from operation_state_mapper import OperationStateMapper
from shift_state_mapper import ShiftStateMapper
from sensor_data_mapper import SensorDataMapper

from requirement_mapper import RequirementMapper
from shift_mapper import ShiftMapper
from operation_mapper import OperationMapper


class EntityQuery(graphene.ObjectType):

	# recital (field lists)

    people = graphene.List(PersonMapper, 
    	id = graphene.String(default_value = ''),
        name = graphene.String(default_value = ''),
        surname = graphene.String(default_value = ''),
        patronymic = graphene.String(default_value = ''),
        phone = graphene.String(default_value = ''),
        department = graphene.String(default_value = ''),
        specialization = graphene.String(default_value = ''))

    departments = graphene.List(DepartmentMapper, 
    	id = graphene.String(default_value = ''),
        name = graphene.String(default_value = ''),
        vk = graphene.String(default_value = ''),
        director = graphene.String(default_value = ''))

    property_types = graphene.List(PropertyTypeMapper, 
    	id = graphene.String(default_value = ''), 
    	desc = graphene.String(default_value = ''),
        name = graphene.String(default_value = ''))

    specializations = graphene.List(SpecializationMapper, 
    	id = graphene.String(default_value = ''), 
    	name = graphene.String(default_value = ''))

    properties = graphene.List(PropertyMapper, 
    	id = graphene.String(default_value = ''), 
    	name = graphene.String(default_value = ''),
        type_ = graphene.String(default_value = ''),
        admission = graphene.String(default_value = ''),
        comissioning = graphene.String(default_value = ''),
        department = graphene.String(default_value = ''))

    system_states = graphene.List(SystemStateMapper, 
    	id = graphene.String(default_value = ''), 
    	desc = graphene.String(default_value = ''),
        name = graphene.String(default_value = ''))

    system_types = graphene.List(SystemTypeMapper, 
    	id = graphene.String(default_value = ''), 
    	desc = graphene.String(default_value = ''),
        name = graphene.String(default_value = ''))

    locations = graphene.List(LocationMapper, 
    	id = graphene.String(default_value = ''), 
    	name = graphene.String(default_value = ''))

    boats = graphene.List(BoatMapper, 
    	id = graphene.String(default_value = ''), 
    	name = graphene.String(default_value = ''), 
        capacity = graphene.Int(default_value = -1))

    sensors = graphene.List(SensorMapper, 
    	id = graphene.String(default_value = ''), 
        name = graphene.String(default_value = ''),
        location = graphene.String(default_value = ''))

    systems = graphene.List(SystemMapper, 
    	id = graphene.String(default_value = ''), 
    	name = graphene.String(default_value = ''),
        serialnumber = graphene.Float(default_value = float('nan')),
        launched = graphene.String(default_value = ''),
        checked = graphene.String(default_value = ''),
        state = graphene.String(default_value = ''),
        supervisor = graphene.String(default_value = ''),
        type_ = graphene.String(default_value = ''))

	# logbook (field lists)

    position = graphene.List(PositionMapper, 
    	id = graphene.String(default_value = ''),
        timestamp = graphene.String(default_value = ''),
        x = graphene.Float(default_value = float('nan')),
        y = graphene.Float(default_value = float('nan')),
        z = graphene.Float(default_value = float('nan')),
        attack_angle = graphene.Float(default_value = float('nan')),
        direction_angle = graphene.Float(default_value = float('nan')),
        speed = graphene.Float(default_value = float('nan')))

    control_action = graphene.List(ControlActionMapper,
        id = graphene.String(default_value = ''),
    	timestamp = graphene.String(default_value = ''),
        mac = graphene.String(default_value = ''),
        user = graphene.String(default_value = ''),
        command = graphene.String(default_value = ''),
        params = graphene.String(default_value = ''),
        result = graphene.String(default_value = ''))

    system_test = graphene.List(SystemTestMapper, 
    	id = graphene.String(default_value = ''),
        timestamp = graphene.String(default_value = ''),
        system = graphene.String(default_value = ''),
        result = graphene.Int(default_value = -1))

    operation_state = graphene.List(OperationStateMapper,
    	id = graphene.String(default_value = ''),
        timestamp = graphene.String(default_value = ''),
        boat = graphene.String(default_value = ''),
        operation = graphene.String(default_value = ''),
        status = graphene.String(default_value = ''),
        distance = graphene.Float(default_value = float('nan')),
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

    shift_state = graphene.List(ShiftStateMapper, 
    	id = graphene.String(default_value = ''),
        timestamp = graphene.String(default_value = ''),
        shift = graphene.String(default_value = ''),
        warninglevel = graphene.String(default_value = ''),
        cartridges = graphene.Int(default_value = -1),
        air = graphene.Int(default_value = -1),
        electricity = graphene.Int(default_value = -1),
        comment = graphene.String(default_value = ''))

    sensor_data = graphene.List(SensorDataMapper, 
    	id = graphene.String(default_value = ''),
        timestamp = graphene.String(default_value = ''),
        sensor = graphene.String(default_value = ''),
        event = graphene.String(default_value = ''),
        meaning = graphene.String(default_value = ''),
        value = graphene.Float(default_value = float('nan')),
        units = graphene.String(default_value = ''))

    # relations (field lists)

    requirements = graphene.List(RequirementMapper, id = graphene.String(default_value = ''), name = graphene.String(default_value = ''),
        specializations = graphene.String(default_value = ''))
    shifts = graphene.List(ShiftMapper, id = graphene.String(default_value = ''),
        start = graphene.String(default_value = ''), end = graphene.String(default_value = ''))
    operations = graphene.List(OperationMapper, id = graphene.String(default_value = ''), name = graphene.String(default_value = ''),
        start = graphene.String(default_value = ''), end = graphene.String(default_value = ''))

    #recital (resolvers)

    def resolve_people(self, info, id, name, surname, patronymic, phone, department, specialization):
        return PersonMapper.eject(id, name, surname, patronymic, phone, department, specialization)

    def resolve_departments(self, info, id, name, vk, director):
    	return DepartmentMapper.eject(id, name, vk, director)

    def resolve_property_types(self, info, id, name, desc):
        return PropertyTypeMapper.eject(id, name, desc)

    def resolve_specializations(self, info, id, name):
    	return SpecializationMapper.eject(id, name)       

    def resolve_properties(self, info, id, name, type_, admission, comissioning, department):
    	return PropertyMapper.eject(id, name, type_, admission, comissioning, department)
        
    def resolve_system_states(self, info, id, name, desc):
        return SystemStateMapper.eject(id, name, desc)

    def resolve_system_types(self, info, id, name, desc):
        return SystemTypeMapper.eject(id, name, desc)

    def resolve_locations(self, info, id, name):
        return LocationMapper.eject(id, name)

    def resolve_boats(self, info, id, name, capacity):
    	return BoatMapper.eject(id, name, capacity if capacity != -1 else None)

    def resolve_sensors(self, info, id, name, location):
        return SensorMapper.eject(id, name, location)

    def resolve_systems(self, info, id, name, launched, checked, serialnumber, state, type_, supervisor):
        return SystemMapper.eject(id, name, launched, checked, serialnumber, state, type_, supervisor)

    #logbook (resolvers)

    def resolve_system_test(self, info, id, timestamp, system, result):
        return SystemTestMapper.eject(id, timestamp, system, result)

    def resolve_control_action(self, info, id, timestamp, mac, user, command, params, result):
        return ControlActionMapper.eject(id, timestamp, mac, user, command, params, result)

    def resolve_position(self, info, id, timestamp, x, y, z, speed, attack_angle, direction_angle):
        return PositionMapper.eject(id, timestamp, x, y, z, speed, attack_angle, direction_angle)

    def resolve_operation_state(self, info, id, timestamp, boat, operation, status, distance, zenith, azimuth, hydrogenium,
        helium, lithium, beryllium, borum,
        carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,
        scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,
        crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,
        stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,
        terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,
        hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,
        plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,
        seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,
        oganesson, comment):
    	return OperationStateMapper.eject(id, timestamp, boat, operation, status, distance, zenith, azimuth, hydrogenium,
	        helium, lithium, beryllium, borum,
	        carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,
	        scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,
	        crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,
	        stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,
	        terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,
	        hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,
	        plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,
	        seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,
	        oganesson, comment)
        
    def resolve_shift_state(self, info, id, timestamp, shift, warninglevel, cartridges, air, electricity, comment):
    	return ShiftStateMapper.eject(id, timestamp, shift, warninglevel, cartridges, air, electricity, comment)

    def resolve_sensor_data(self, info, id, timestamp, sensor, event, meaning, value, units):
        return SensorDataMapper.eject(id, timestamp, sensor, event, meaning, value, units)

    #relations (resolvers)

    def resolve_requirements(self, info, id, name, specializations):
        return RequirementMapper.eject(id, name, specializations)

    def resolve_shifts(self, info, id, start, end):
        return ShiftMapper.eject(id, start, end);

    def resolve_operations(self, info, id, name, start, end):
        return OperationMapper.eject(id, name, start, end)