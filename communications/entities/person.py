import sys, re

from neomodel import StructuredNode, IntegerProperty, StringProperty, ArrayProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, One

from department import Department
from operation import Operation
from shift import Shift

sys.path.append('adapters')

import mongo_adapter

class Person(StructuredNode):
    ident = ArrayProperty(IntegerProperty(), unique_index = True, required = True)

    controlled = RelationshipTo('Department', 'DIRECTOR', cardinality=One)

    executor = RelationshipTo('Operation', 'EXECUTOR')
    head = RelationshipTo('Operation', 'HEAD', cardinality=One)

    worker = RelationshipTo('Shift', 'WORKER')
    chief = RelationshipTo('Shift', 'CHIEF', cardinality=One)

    def __init__(self, *args, **kwargs):
        if isinstance(kwargs['ident'], str):
            if mongo_adapter.is_valid_foreign_id('user_test', kwargs['ident']):
                kwargs['ident'] = mongo_adapter.mongo_str_id_to_int(kwargs['ident'])
            else:
                raise ValueError('invalid person id')

        super(Person, self).__init__(self, *args, **kwargs)

    @property
    def ident_hex(self):
        return mongo_adapter.int_to_mongo_str_id(self.ident) if self.ident else None
    