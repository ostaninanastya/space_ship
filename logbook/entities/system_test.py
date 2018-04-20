import sys, os
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

sys.path.append('adapters')

import mongo_adapter

import configparser

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

SYSTEMS_COLLECTION_NAME = os.environ.get('SYSTEMS_COLLECTION_NAME') or config['MONGO']['systems_collection_name']

class SystemTest(Model):
    date = columns.Date(required = True, partition_key = True)
    time = columns.Time(required = True, primary_key = True)
    
    system_id = columns.Bytes(required = True, primary_key = True)
    result = columns.TinyInt(required = True)

    def validate(self):
        super(SystemTest, self).validate()
        
        if self.result < 0 or self.result > 100:
            raise ValidationError('not a valid test result value')

        SystemTest.validate_system_id(self.system_id)

    @staticmethod
    def validate_system_id(id):
        if len(id) != 12 or not mongo_adapter.is_valid_foreign_id(SYSTEMS_COLLECTION_NAME, id.hex()):
            raise ValidationError('not a valid system id')