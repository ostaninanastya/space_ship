from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, One

class Department(StructuredNode):
    ident = IntegerProperty(unique_index = True)
    name = StringProperty()
    room = IntegerProperty(unique_index = True)

    shifts = RelationshipFrom('Shift', 'INCORPORATION')
    operations = RelationshipFrom('Operation', 'INCORPORATION')

    controller = RelationshipFrom('Person', 'DIRECTOR', cardinality=One)