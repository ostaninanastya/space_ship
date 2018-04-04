import sys

from neomodel import StructuredNode, IntegerProperty, StringProperty, ArrayProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, One

sys.path.append('adapters')

import mongo_adapter

class Department(StructuredNode):
    ident = ArrayProperty(IntegerProperty(), unique_index = True, required = True)

    shifts = RelationshipFrom('shift.Shift', 'INCORPORATION')
    operations = RelationshipFrom('operation.Operation', 'INCORPORATION')

    controller = RelationshipFrom('person.Person', 'DIRECTOR', cardinality=One)

    def __init__(self, *args, **kwargs):
        kwargs['ident'] = mongo_adapter.validate_id('department_test', kwargs['ident'])
        super(Department, self).__init__(self, *args, **kwargs)

    @property
    def ident_hex(self):
        return mongo_adapter.int_to_mongo_str_id(self.ident) if self.ident else None