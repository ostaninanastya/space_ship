import sys, os

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
    result += get_mutation_description(specialization_manipulator.EradicateSpecialization)
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