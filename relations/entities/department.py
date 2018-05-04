import sys, os

from neomodel import StructuredNode, IntegerProperty, StringProperty, ArrayProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, One

sys.path.append('adapters')

import mongo_adapter

import configparser

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

DEPARTMENTS_COLLECTION_NAME = os.environ.get('DEPARTMENTS_COLLECTION_NAME') or config['MONGO']['departments_collection_name']

class Department(StructuredNode):
    ident = ArrayProperty(IntegerProperty(), unique_index = True, required = True)

    shifts = RelationshipFrom('shift.Shift', 'INCORPORATION')
    operations = RelationshipFrom('operation.Operation', 'INCORPORATION')

    controller = RelationshipFrom('person.Person', 'DIRECTOR', cardinality=One)

    def __init__(self, *args, **kwargs):
        kwargs['ident'] = mongo_adapter.validate_id('departments', kwargs['ident'])
        super(Department, self).__init__(self, *args, **kwargs)

    @property
    def ident_hex(self):
        return mongo_adapter.int_to_mongo_str_id(self.ident) if self.ident else None