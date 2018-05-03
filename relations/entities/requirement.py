import sys, os

from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, ArrayProperty, JSONProperty, One

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/adapters')

import mongo_adapter

import configparser

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

SPECIALIZATIONS_COLLECTION_NAME = os.environ.get('SPECIALIZATIONS_COLLECTION_NAME') or config['MONGO']['specializations_collection_name']

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
                self.content[i]['specialization'] = mongo_adapter.validate_id(SPECIALIZATIONS_COLLECTION_NAME, self.content[i]['specialization'])

    @property
    def content_hexes(self):
        hexes = []
        for i in range(len(self.content)):
            hexes.append(mongo_adapter.int_to_mongo_str_id(self.content[i]['specialization']) if self.content[i]['specialization'] else None)
        return hexes

    @staticmethod
    def specialization_id_to_neo4j_format(id):
        return mongo_adapter.validate_id(SPECIALIZATIONS_COLLECTION_NAME, id)