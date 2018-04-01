from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, One

class Operation(StructuredNode):
    ident = UniqueIdProperty()

    department = RelationshipTo('Department', 'INCORPORATION')
    requirement = RelationshipFrom('Requirement', 'USER')

    persons = RelationshipFrom('Person', 'EXECUTOR')
    head = RelationshipFrom('Person', 'HEAD', cardinality=One)