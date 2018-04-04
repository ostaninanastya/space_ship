import sys, re

from neomodel import StructuredNode, IntegerProperty, StringProperty, ArrayProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, One

sys.path.append('adapters')

import mongo_adapter

class Person(StructuredNode):
    ident = ArrayProperty(IntegerProperty(), unique_index = True, required = True)

    controlled = RelationshipTo('department.Department', 'DIRECTOR', cardinality = One)

    executor = RelationshipTo('operation.Operation', 'EXECUTOR')
    head = RelationshipTo('operation.Operation', 'HEAD', cardinality=One)

    worker = RelationshipTo('shift.Shift', 'WORKER')
    chief = RelationshipTo('shift.Shift', 'CHIEF', cardinality=One)

    def __init__(self, *args, **kwargs):
        kwargs['ident'] = mongo_adapter.validate_id('user_test', kwargs['ident'])
        super(Person, self).__init__(self, *args, **kwargs)

    @property
    def ident_hex(self):
        return mongo_adapter.int_to_mongo_str_id(self.ident) if self.ident else None
    