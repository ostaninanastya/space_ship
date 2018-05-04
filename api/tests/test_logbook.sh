#! /bin/bash
echo 'positions'
python3 positions.py -v
echo 'system_tests'
python3 system_tests.py -v
echo 'sensor_data'
python3 sensor_data.py -v
echo 'shift_states'
python3 shift_states.py -v
echo 'control actions'
python3 control_actions.py -v
echo 'operation states'
python3 operation_states.py -v