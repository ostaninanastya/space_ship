from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, One

class Requirement(StructuredNode):
    ident = UniqueIdProperty()
    name = StringProperty()

    operations = RelationshipTo('Operation', 'USER')
    shift = RelationshipTo('Shift', 'USER')