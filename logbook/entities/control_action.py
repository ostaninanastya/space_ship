import sys, os
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

sys.path.append(os.environ.get('SPACE_SHIP_HOME') + '/logbook/adapters')

import mongo_adapter

import configparser

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

PEOPLE_COLLECTION_NAME = os.environ.get('PEOPLE_COLLECTION_NAME') or config['MONGO']['people_collection_name']

class ControlAction(Model):
    date = columns.Date(required = True, partition_key = True)
    time = columns.Time(required = True, primary_key = True)
    
    mac_address = columns.Bytes(required = True, primary_key = True)
    user_id = columns.Bytes(required = True, primary_key = True)
    
    command = columns.Text(required = True)
    params = columns.Text()
    result = columns.Text()

    def validate(self):
        super(ControlAction, self).validate()
        ControlAction.validate_mac_address(self.mac_address)
        ControlAction.validate_user_id(self.user_id)

    @staticmethod
    def validate_mac_address(id):
        if len(id) != 6:
            raise ValidationError('not a valid mac address')
        return id

    @staticmethod
    def validate_user_id(id):
        if len(id) != 12 or not mongo_adapter.is_valid_foreign_id(PEOPLE_COLLECTION_NAME, id.hex()):
            raise ValidationError('not a valid user id')
        return id
