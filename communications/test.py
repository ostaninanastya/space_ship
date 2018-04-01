from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, One	

import os
import configparser

configp = configparser.ConfigParser()
configp.read('../databases.config')

NEO4J_DB_URL = os.environ.get('NEO4J_DB_URL') if os.environ.get('NEO4J_DB_URL') else configp['NEO4J']['host']
NEO4J_DB_PORT = int(os.environ.get('NEO4J_DB_PORT') if os.environ.get('NEO4J_DB_PORT') else configp['NEO4J']['port'])

USERNAME = os.environ.get('NEO4J_DB_USERNAME') if os.environ.get('NEO4J_DB_USERNAME') else configp['NEO4J']['username']
PASSWORD = os.environ.get('NEO4J_DB_PASSWORD') if os.environ.get('NEO4J_DB_PASSWORD') else configp['NEO4J']['password']

config.DATABASE_URL = 'bolt://' + USERNAME + ':' + PASSWORD + '@' + NEO4J_DB_URL + ':' + str(NEO4J_DB_PORT)

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
    ident = UniqueIdProperty()

    department = RelationshipTo('Department', 'INCORPORATION')
    requirement = RelationshipFrom('Requirement', 'USER')

    persons = RelationshipFrom('Person', 'EXECUTOR')
    head = RelationshipFrom('Person', 'HEAD', cardinality=One)

class Shift(StructuredNode):
    ident = UniqueIdProperty()

    requirement = RelationshipFrom('Requirement', 'USER')
    department = RelationshipTo('Department', 'INCORPORATION')

    workers = RelationshipFrom('Person', 'WORKER')
    chief = RelationshipFrom('Person', 'CHIEF', cardinality=One)

class Requirement(StructuredNode):
    ident = UniqueIdProperty()
    name = StringProperty()

    operations = RelationshipTo('Operation', 'USER')
    shift = RelationshipTo('Shift', 'USER')

buzz = Person(ident = 1).save()
woody = Person(ident = 2).save()
jessie = Person(ident = 3).save()
dangerous_operation = Operation().save()

buzz.executor.connect(dangerous_operation)
woody.executor.connect(dangerous_operation)
jessie.head.connect(dangerous_operation)

hamm = Person(ident = 4).save()
bullseye = Person(ident = 5).save()
rex = Person(ident = 6).save()
next_shift = Shift().save()

hamm.worker.connect(next_shift)
bullseye.worker.connect(next_shift)
rex.chief.connect(next_shift)

base_req = Requirement(name='Base requirement').save()
base_req.operations.connect(dangerous_operation)

low_req = Requirement(name='Low requirement').save()
low_req.shift.connect(next_shift)

main_department = Department(ident = 123, name = 'Main department', room = 324).save()
dangerous_operation.department.connect(main_department)
next_shift.department.connect(main_department)

stretch = Person(ident = 7).save()
stretch.controlled.connect(main_department)

