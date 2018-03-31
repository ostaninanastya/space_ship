import sys, os
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

sys.path.append('adapters')

import mongo_adapter

class SystemTest(Model):
    time = columns.DateTime(required = True, primary_key = True)
    system_id = columns.Bytes(required = True, primary_key = True)
    result = columns.TinyInt(required = True)

    def validate(self):
        super(SystemTest, self).validate()
        
        if self.result < 0 or self.result > 100:
            raise ValidationError('not a valid test result value')

        if len(self.system_id) != 12 or not mongo_adapter.is_valid_foreign_id('system_test', self.system_id.hex()):
        	raise ValidationError('not a valid system id')