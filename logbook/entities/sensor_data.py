import sys, os
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

sys.path.append('adapters')

import mongo_adapter
from data_adapters import get_strings

EVENTS = get_strings(os.environ['SPACE_SHIP_HOME'] + '/logbook/enums/sensor_events')
VALUE_TYPES = get_strings(os.environ['SPACE_SHIP_HOME'] + '/logbook/enums/value_types')
VALUE_UNITS = get_strings(os.environ['SPACE_SHIP_HOME'] + '/logbook/enums/units')

import configparser

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

SENSORS_COLLECTION_NAME = os.environ.get('SENSORS_COLLECTION_NAME') or config['MONGO']['sensors_collection_name']

class SensorData(Model):
    date = columns.Date(required = True, partition_key = True)
    time = columns.Time(required = True, primary_key = True)

    source_id = columns.Bytes(required = True)
    event = columns.Text(required = True)
    value_name = columns.Text(required = True)
    value = columns.Double(required = True)
    units = columns.Text(required = True)

    def validate(self):
        super(SensorData, self).validate()
        SensorData.validate_source_id(self.source_id)
        SensorData.validate_event(self.event)
        SensorData.validate_value_name(self.value_name)
        SensorData.validate_units(self.units)

    @staticmethod
    def validate_source_id(id):
        if len(source_id) != 12 or not mongo_adapter.is_valid_foreign_id(SENSORS_COLLECTION_NAME, source_id.hex()):
            raise ValidationError('not a valid source id')
        return id

    @staticmethod
    def validate_event(event):
        if event not in EVENTS:
            raise ValidationError('not a valid event')

    @staticmethod
    def validate_value_name(value_name):
        if value_name not in VALUE_TYPES:
            raise ValidationError('not a valid value type')

    @staticmethod
    def validate_units(units):
        if units not in VALUE_UNITS:
            raise ValidationError('not a valid value units')