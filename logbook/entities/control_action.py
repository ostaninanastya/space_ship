import sys, os
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/logbook/adapters')

import mongo_adapter

class ControlAction(Model):
    date = columns.Date(required = True, partition_key = True)
    time = columns.Time(required = True, primary_key = True)
    
    mac_address = columns.Bytes(required = True)
    user_id = columns.Bytes(required = True)
    
    command = columns.Text(required = True)
    params = columns.Text()
    result = columns.Text()

    def validate(self):
        super(ControlAction, self).validate()
        
        if len(self.mac_address) != 6:
            raise ValidationError('not a valid mac address')

        if len(self.user_id) != 12 or not mongo_adapter.is_valid_foreign_id('people_test', self.user_id.hex()):
        	raise ValidationError('not a valid user id')