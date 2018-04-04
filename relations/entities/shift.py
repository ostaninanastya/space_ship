import datetime

from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, DateTimeProperty, RelationshipFrom, UniqueIdProperty, config, One

class Shift(StructuredNode):
    ident = UniqueIdProperty()

    start = DateTimeProperty(default = lambda: datetime.datetime.now())
    end = DateTimeProperty(default = lambda: datetime.datetime.now() + datetime.timedelta(days = 2))

    requirement = RelationshipFrom('requirement.Requirement', 'USER')
    department = RelationshipTo('department.Department', 'INCORPORATION')

    workers = RelationshipFrom('person.Person', 'WORKER')
    chief = RelationshipFrom('person.Person', 'CHIEF', cardinality=One)