import sys, os
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

sys.path.append('adapters')

import mongo_adapter
from data_adapters import get_strings

EVENTS = get_strings('enums/sensor_events')
VALUE_TYPES = get_strings('enums/value_types')
VALUE_UNITS = get_strings('enums/units')

class SensorData(Model):
    time = columns.DateTime(required = True, primary_key = True)
    source_id = columns.Bytes(required = True, primary_key = True)
    event = columns.Text(required = True)
    value_name = columns.Text(required = True)
    value = columns.Double(required = True)
    units = columns.Text(required = True)

    def validate(self):
        super(SensorData, self).validate()

        if len(self.source_id) != 12 or not mongo_adapter.is_valid_foreign_id('source_test', self.source_id.hex()):
        	raise ValidationError('not a valid source id')

        if self.event not in EVENTS:
        	raise ValidationError('not a valid event')

        if self.value_name not in VALUE_TYPES:
        	raise ValidationError('not a valid value type')

        if self.units not in VALUE_UNITS:
        	raise ValidationError('not a valid value units')

