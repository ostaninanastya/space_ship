from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, One

class Shift(StructuredNode):
    ident = UniqueIdProperty()

    requirement = RelationshipFrom('Requirement', 'USER')
    department = RelationshipTo('Department', 'INCORPORATION')

    workers = RelationshipFrom('Person', 'WORKER')
    chief = RelationshipFrom('Person', 'CHIEF', cardinality=One)