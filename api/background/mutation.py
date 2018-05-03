import sys, os

import graphene

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

import position_manipulator
import control_action_manipulator
import system_test_manipulator
import sensor_data_manipulator
import shift_state_manipulator
import operation_state_manipulator

import shift_manipulator
import operation_manipulator
import requirement_manipulator

class EntityMutation(graphene.ObjectType):

	# recital
    
    create_location = location_manipulator.CreateLocation.Field()
    remove_location = location_manipulator.RemoveLocation.Field()
    eradicate_location = location_manipulator.EradicateLocation.Field()
    update_locations = location_manipulator.UpdateLocations.Field()

    create_sensor = sensor_manipulator.CreateSensor.Field()
    remove_sensor = sensor_manipulator.RemoveSensor.Field()
    update_sensors = sensor_manipulator.UpdateSensors.Field()

    create_department = department_manipulator.CreateDepartment.Field()
    remove_department = department_manipulator.RemoveDepartment.Field()
    eradicate_department = department_manipulator.EradicateDepartment.Field()
    update_departments = department_manipulator.UpdateDepartments.Field()

    create_specialization = specialization_manipulator.CreateSpecialization.Field()
    remove_specialization = specialization_manipulator.RemoveSpecialization.Field()
    eradicate_specialization = specialization_manipulator.EradicateSpecialization.Field()
    update_specializations = specialization_manipulator.UpdateSpecializations.Field()

    create_person = person_manipulator.CreatePerson.Field()
    remove_person = person_manipulator.RemovePerson.Field()
    eradicate_person = person_manipulator.EradicatePerson.Field()
    update_people = person_manipulator.UpdatePeople.Field()

    create_boat = boat_manipulator.CreateBoat.Field()
    remove_boat = boat_manipulator.RemoveBoat.Field()
    update_boats = boat_manipulator.UpdateBoats.Field()

    create_systemtype = system_type_manipulator.CreateSystemType.Field()
    remove_systemtype = system_type_manipulator.RemoveSystemType.Field()
    eradicate_systemtype = system_type_manipulator.EradicateSystemType.Field()
    update_systemtypes = system_type_manipulator.UpdateSystemTypes.Field()

    create_systemstate = system_state_manipulator.CreateSystemState.Field()
    remove_systemstate = system_state_manipulator.RemoveSystemState.Field()
    eradicate_systemstate = system_state_manipulator.EradicateSystemState.Field()
    update_systemstates = system_state_manipulator.UpdateSystemStates.Field()

    create_propertytype = property_type_manipulator.CreatePropertyType.Field()
    remove_propertytype = property_type_manipulator.RemovePropertyType.Field()
    eradicate_propertytype = property_type_manipulator.EradicatePropertyType.Field()
    update_propertytypes = property_type_manipulator.UpdatePropertyTypes.Field()

    create_system = system_manipulator.CreateSystem.Field()
    remove_system = system_manipulator.RemoveSystem.Field()
    update_systems = system_manipulator.UpdateSystems.Field()

    create_property = property_manipulator.CreateProperty.Field()
    remove_property = property_manipulator.RemoveProperty.Field()
    update_properties = property_manipulator.UpdateProperties.Field()

    # logbook

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

    # relations

    create_shift = shift_manipulator.CreateShift.Field()
    remove_shift = shift_manipulator.RemoveShift.Field()
    update_shifts = shift_manipulator.UpdateShifts.Field()

    create_operation = operation_manipulator.CreateOperation.Field()
    remove_operation = operation_manipulator.RemoveOperation.Field()
    update_operations = operation_manipulator.UpdateOperations.Field()

    create_requirement = requirement_manipulator.CreateRequirement.Field()
    remove_requirement = requirement_manipulator.RemoveRequirement.Field()
    update_requirements = requirement_manipulator.UpdateRequirements.Field()