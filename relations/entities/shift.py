import datetime
from datetime import timezone

from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, DateTimeProperty, RelationshipFrom, UniqueIdProperty, config, One

class Shift(StructuredNode):
    ident = UniqueIdProperty()

    start = DateTimeProperty(default = lambda: datetime.datetime.now())
    end = DateTimeProperty(default = lambda: datetime.datetime.now() + datetime.timedelta(days = 2))

    requirement = RelationshipFrom('requirement.Requirement', 'USER')
    department = RelationshipTo('department.Department', 'INCORPORATION')

    workers = RelationshipFrom('person.Person', 'WORKER')
    chief = RelationshipFrom('person.Person', 'CHIEF', cardinality=One)

    def __init__(self, *args, **kwargs):
        super(Shift, self).__init__(self, *args, **kwargs)
    
    def validate(self):
        self.validate_dates()
        return self

    def validate_dates(self):
        self.start = self.start.replace(tzinfo=timezone.utc)
        self.end = self.end.replace(tzinfo=timezone.utc)
        if (self.end - self.start).total_seconds() < 0:
            raise ValueError('End datetime can\'t be less than start datetime')