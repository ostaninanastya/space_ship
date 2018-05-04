import unittest
from urllib.request import urlopen
import json

MIN = 3

class TestSearchMethod(unittest.TestCase):

    def get_result_length(self, collection, fields):
        result = urlopen('http://localhost:1881/api/{0}/fields={1}'.format(collection, ','.join(fields)))
        return len(json.loads(result.read())[collection])

    # *** plain selection tests ***

    # - recital

    def test_get_all_people_names(self):        
        assert self.get_result_length('people', ['name']) > MIN

    def test_get_all_department_vks(self):
        assert self.get_result_length('departments', ['vk']) > MIN

    def test_get_all_property_type_names(self):        
        assert self.get_result_length('propertyTypes', ['name']) > MIN

    def test_get_all_specialization_ids(self):        
        assert self.get_result_length('specializations', ['id']) > MIN

    def test_get_all_property_names(self):        
        assert self.get_result_length('properties', ['name']) > MIN

    def test_get_all_system_state_names(self):
        assert self.get_result_length('systemStates', ['name']) > MIN

    def test_get_all_system_type_names(self):
        assert self.get_result_length('systemTypes', ['name']) > MIN

    def test_get_all_location_names(self):
        assert self.get_result_length('locations', ['name']) > MIN

    def test_get_all_boats_names(self):
        assert self.get_result_length('boats', ['name']) > MIN

    def test_get_all_sensor_names(self):
        assert self.get_result_length('sensors', ['name']) > MIN

    def test_get_all_system_names(self):
        assert self.get_result_length('systems', ['name']) > MIN

    # - logbook

    def test_get_all_system_test_dates(self):        
        assert self.get_result_length('systemTest', ['date']) > MIN

    def test_get_all_control_action_dates(self):        
        assert self.get_result_length('controlAction', ['date']) > MIN

    def test_get_all_position_dates(self):        
        assert self.get_result_length('position', ['date']) > MIN

    def test_get_all_operation_state_dates(self):        
        assert self.get_result_length('operationState', ['date']) > MIN

    def test_get_all_shift_state_dates(self):        
        assert self.get_result_length('shiftState', ['date']) > MIN

    def test_get_all_sensor_data_dates(self):        
        assert self.get_result_length('sensorData', ['date']) > MIN

    # - relations

    def test_get_all_operation_idents(self):        
        assert self.get_result_length('operations', ['id']) > MIN

    def test_get_all_shift_idents(self):        
        assert self.get_result_length('shifts', ['id']) > MIN

    def test_get_all_requirement_idents(self):        
        assert self.get_result_length('requirements', ['id']) > MIN

if __name__ == '__main__':
    unittest.main()