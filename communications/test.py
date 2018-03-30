from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, config, One	

import os

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

config.DATABASE_URL = 'bolt://' + USERNAME + ':' + PASSWORD + '@localhost:7687'

class Department(StructuredNode):
    ident = IntegerProperty(unique_index = True)
    name = StringProperty()
    room = IntegerProperty(unique_index = True)

    shifts = RelationshipFrom('Shift', 'INCORPORATION')
    operations = RelationshipFrom('Operation', 'INCORPORATION')

    controller = RelationshipFrom('Person', 'DIRECTOR', cardinality=One)

class Person(StructuredNode):
    ident = IntegerProperty(unique_index = True)

    controlled = RelationshipTo('Department', 'DIRECTOR', cardinality=One)

    executor = RelationshipTo('Operation', 'EXECUTOR')
    head = RelationshipTo('Operation', 'HEAD', cardinality=One)

    worker = RelationshipTo('Shift', 'WORKER')
    chief = RelationshipTo('Shift', 'CHIEF', cardinality=One)

class Operation(StructuredNode):
    ident = IntegerProperty(unique_index = True)

    department = RelationshipTo('Department', 'INCORPORATION')
    requirement = RelationshipFrom('Requirement', 'USER')

    persons = RelationshipFrom('Person', 'EXECUTOR')
    head = RelationshipFrom('Person', 'HEAD', cardinality=One)

class Shift(StructuredNode):
    ident = IntegerProperty(unique_index = True)

    requirement = RelationshipFrom('Requirement', 'USER')
    department = RelationshipTo('Department', 'INCORPORATION')

    workers = RelationshipFrom('Person', 'WORKER')
    chief = RelationshipFrom('Person', 'CHIEF', cardinality=One)

class Requirement(StructuredNode):
    ident = IntegerProperty(unique_index = True)
    name = StringProperty()

    operations = RelationshipTo('Operation', 'USER')
    shift = RelationshipTo('Shift', 'USER')

buzz = Person(ident = 1488).save()
woody = Person(ident = 228).save()
jessie = Person(ident = 666).save()
dangerous_operation = Operation(ident = 17).save()

buzz.executor.connect(dangerous_operation)
woody.executor.connect(dangerous_operation)
jessie.head.connect(dangerous_operation)

hamm = Person(ident = 13).save()
bullseye = Person(ident = 18).save()
rex = Person(ident = 19).save()
next_shift = Shift(ident = 77).save()

hamm.worker.connect(next_shift)
bullseye.worker.connect(next_shift)
rex.chief.connect(next_shift)

base_req = Requirement(ident = 1, name='Base requirement').save()
base_req.operations.connect(dangerous_operation)

low_req = Requirement(ident = 1, name='Low requirement').save()
low_req.shift.connect(next_shift)

main_department = Department(ident = 123, name = 'Main department', room = 324).save()
dangerous_operation.department.connect(main_department)
next_shift.department.connect(main_department)

stretch = Person(ident = 256).save()
stretch.controlled.connect(main_department)

