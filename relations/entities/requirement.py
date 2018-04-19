import sys, os

from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, ArrayProperty, JSONProperty, One

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/adapters')

import mongo_adapter

class Requirement(StructuredNode):
    ident = UniqueIdProperty()
    
    name = StringProperty()
    content = ArrayProperty(JSONProperty(), required=True)

    operations = RelationshipTo('operation.Operation', 'USER')
    shift = RelationshipTo('shift.Shift', 'USER')

    def __init__(self, *args, **kwargs):
        super(Requirement, self).__init__(self, *args, **kwargs)
        if isinstance(self.content, list):
	        for i in range(len(self.content)):
	            self.content[i]['ident'] = mongo_adapter.validate_id('spec_test', self.content[i]['ident'])

    @property
    def content_hexes(self):
        hexes = []
        for i in range(len(self.content)):
            hexes.append(mongo_adapter.int_to_mongo_str_id(self.content[i]['ident']) if self.content[i]['ident'] else None)
        return hexes

    @staticmethod
    def specialization_id_to_neo4j_format(id):
        return mongo_adapter.validate_id('spec_test', id)