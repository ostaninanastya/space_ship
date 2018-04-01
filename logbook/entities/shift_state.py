import sys, os
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

sys.path.append('adapters')

import neo4j_adapter
from data_adapters import get_strings

WARNING_LEVELS = get_strings('enums/shift_warning_levels')

class ShiftState(Model):
    time = columns.DateTime(required = True, primary_key = True)
    shift_id = columns.Bytes(required = True, primary_key = True)
    warning_level = columns.Text(required = True)

    remaining_cartridges = columns.TinyInt(required = True)
    remaining_air = columns.TinyInt(required = True)
    remaining_electricity = columns.TinyInt(required = True)

    comment = columns.Text()

    def validate(self):
        super(ShiftState, self).validate()
        
        if len(self.shift_id) != 16 or not neo4j_adapter.is_valid_foreign_id('Shift', self.shift_id.hex()):
            raise ValidationError('not a valid shift id')

        if self.warning_level not in WARNING_LEVELS:
            print(self.warning_level)
            print(WARNING_LEVELS)
            raise ValidationError('not a warning level')

        if self.remaining_cartridges < 0 or self.remaining_cartridges > 100:
            raise ValidationError('not a valid remaining cartridges value')

        if self.remaining_air < 0 or self.remaining_air > 100:
            raise ValidationError('not a valid remaining air value')

        if self.remaining_electricity < 0 or self.remaining_electricity > 100:
            raise ValidationError('not a valid remaining electricity value')