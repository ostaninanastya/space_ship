import sys, os

import datetime, math
import re
import configparser
from bson.objectid import ObjectId

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

def parse_date_parameter(date):
    return None if not date else datetime.datetime.strptime(date, DATE_PATTERN).date()

def parse_time_parameter(time):
    return None if not time else datetime.datetime.strptime(time, TIME_PATTERN).time()

def parse_timestamp_parameter(timestamp):
    return None if not timestamp else datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)

def stringify_timestamp_parameter(timestamp):
    return None if not timestamp else timestamp.strftime(TIMESTAMP_PATTERN)

def parse_bytes_parameter(value):
    return None if not value else string_to_bytes(value)

def parse_objectid_parameter(value):
    return None if not value else ObjectId(value)

def parse_float_parameter(value):
    return value if not math.isnan(value) else None


def get_strings(filename):
    with open(filename) as handle:
        content = handle.readlines()

    content = [x.strip() for x in content]
    result = []
    for item in content:
        if item != '':
            result.append(item)

    return result

def string_to_datetime(source_string):
    return datetime.datetime.fromtimestamp(int(float(source_string)))

def string_to_bytes(source_string):
    return bytearray.fromhex(' '.join(re.findall('..', source_string)))


def get_file_content(filename, get_tuple):
    with open(filename) as handle:
        content = handle.readlines()

    content = [x.strip() for x in content]
    result = []
    for item in content:
        if item != '':
            result.append(get_tuple(item))

    return result

def get_position_tuple(string_to_parse):
    items = string_to_parse.split(' :: ')

    return (
        string_to_datetime(items[0]), \
        float(items[1]), \
        float(items[2]), \
        float(items[3]), \
        float(items[4]), \
        float(items[5]), \
        float(items[6]) \
    )

def get_positions(filename):
    return get_file_content(filename, get_position_tuple)

def get_system_test_tuple(string_to_parse):
    items = string_to_parse.split(' :: ')

    return (
        string_to_datetime(items[0]), \
        string_to_bytes(items[1]), \
        int(float(items[2]))
    )

def get_system_tests(filename):
    return get_file_content(filename, get_system_test_tuple)

def get_control_action_tuple(string_to_parse):
    items = string_to_parse.split(' :: ')

    return (
        string_to_datetime(items[0]), \
        string_to_bytes(items[1]), \
        string_to_bytes(items[2]), \
        items[3], \
        items[4], \
        items[5]
    )

def get_control_actions(filename):
    return get_file_content(filename, get_control_action_tuple)

def get_sensor_data_tuple(string_to_parse):
    items = string_to_parse.split(' :: ')

    return (
        string_to_datetime(items[0]), \
        string_to_bytes(items[1]), \
        items[2], \
        items[3], \
        float(items[4]), \
        items[5]
    )

def get_sensors_data(filename):
    return get_file_content(filename, get_sensor_data_tuple)

def get_shift_state_tuple(string_to_parse):
    items = [x.strip() for x in string_to_parse.split('::')]

    return (
        string_to_datetime(items[0]), \
        string_to_bytes(items[1]), \
        items[2], \
        int(float(items[3])), \
        int(float(items[4])), \
        int(float(items[5])), \
        items[6]
    )

def get_shift_states(filename):
    return get_file_content(filename, get_shift_state_tuple)

def get_operation_state_tuple(string_to_parse):
    items = [x.strip() for x in string_to_parse.split('::')]

    result = [string_to_datetime(items[0]), string_to_bytes(items[1]), string_to_bytes(items[2]), items[3]]

    i = 4

    while (i < 125):
        result.append(float(items[i]))
        i += 1

    result.append(items[125])

    return tuple(result)

def get_operation_states(filename):
    return get_file_content(filename, get_operation_state_tuple)