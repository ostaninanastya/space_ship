import sys, os
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

sys.path.append('adapters')

import neo4j_adapter
from data_adapters import get_strings

WARNING_LEVELS = get_strings(os.environ['SPACE_SHIP_HOME'] + '/logbook/enums/shift_warning_levels')

class ShiftState(Model):
    date = columns.Date(required = True, partition_key = True)
    time = columns.Time(required = True, primary_key = True)
    
    shift_id = columns.Bytes(required = True)
    warning_level = columns.Text(required = True)

    remaining_cartridges = columns.TinyInt(required = True)
    remaining_air = columns.TinyInt(required = True)
    remaining_electricity = columns.TinyInt(required = True)

    comment = columns.Text()

    def validate(self):
        super(ShiftState, self).validate()
        
        ShiftState.validate_shift_id(self.shift_id)
        ShiftState.validate_warning_level(self.warning_level)
        ShiftState.validate_remaining_quantity(self.remaining_cartridges, 'remaining cartridges')
        ShiftState.validate_remaining_quantity(self.remaining_air, 'remaining air')
        ShiftState.validate_remaining_quantity(self.remaining_electricity, 'remaining electricity')

    @staticmethod
    def validate_shift_id(shift_id):
        if len(shift_id) != 16 or not neo4j_adapter.is_valid_foreign_id('Shift', shift_id.hex()):
            raise ValidationError('not a valid shift id')
        return shift_id

    @staticmethod
    def validate_warning_level(warning_level):
        if warning_level not in WARNING_LEVELS:
            raise ValidationError('not a warning level')
        return warning_level

    @staticmethod
    def validate_remaining_quantity(remaining_quantity, message):
        if remaining_quantity < 0 or remaining_quantity > 100:
            raise ValidationError('not a valid {0} value'.format(message))
        return remaining_quantity