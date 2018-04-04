import datetime

from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, DateTimeProperty, RelationshipFrom, UniqueIdProperty, config, One

class Operation(StructuredNode):
    ident = UniqueIdProperty()

    name = StringProperty()

    start = DateTimeProperty(default = lambda: datetime.datetime.now())
    end = DateTimeProperty(default = lambda: datetime.datetime.now() + datetime.timedelta(days = 14))

    department = RelationshipTo('department.Department', 'INCORPORATION')
    requirement = RelationshipFrom('requirement.Requirement', 'USER')

    persons = RelationshipFrom('person.Person', 'EXECUTOR')
    head = RelationshipFrom('person.Person', 'HEAD', cardinality = One)