import datetime

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
        datetime.datetime.fromtimestamp(int(float(items[0]))), \
        float(items[1]), \
        float(items[2]), \
        float(items[3]), \
        float(items[4]), \
        float(items[5]), \
        float(items[6]) \
    )

def get_positions(filename):
    return get_file_content(filename, get_position_tuple)

def get_system_state_tuple(string_to_parse):
    items = string_to_parse.split(' :: ')

    return (
        datetime.datetime.fromtimestamp(int(float(items[0]))), \
        items[1], \
        int(items[2]), \
        items[3]
    )

def get_system_states(filename):
    return get_file_content(filename, get_system_state_tuple)

def get_control_action_tuple(string_to_parse):
    items = string_to_parse.split(' :: ')

    return (
        datetime.datetime.fromtimestamp(int(float(items[0]))), \
        items[1], \
        items[2], \
        items[3], \
        items[4], \
        items[5]
    )

def get_control_actions(filename):
    return get_file_content(filename, get_control_action_tuple)

def get_sensor_data_tuple(string_to_parse):
    items = string_to_parse.split(' :: ')

    return (
        datetime.datetime.fromtimestamp(int(float(items[0]))), \
        items[1], \
        items[2], \
        items[3], \
        items[4], \
        float(items[5]), \
        items[6]
    )

def get_sensors_data(filename):
    return get_file_content(filename, get_sensor_data_tuple)