from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, config, One	

import os

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

config.DATABASE_URL = 'bolt://' + USERNAME + ':' + PASSWORD + '@localhost:7687'

class Person(StructuredNode):
    ident = IntegerProperty(unique_index = True)
    executor = RelationshipTo('Operation', 'EXECUTOR')
    head = RelationshipTo('Operation', 'HEAD', cardinality=One)

    worker = RelationshipTo('Shift', 'WORKER')
    chief = RelationshipTo('Shift', 'CHIEF', cardinality=One)

class Operation(StructuredNode):
    ident = IntegerProperty(unique_index = True)
    persons = RelationshipFrom('Person', 'EXECUTOR')
    head = RelationshipFrom('Person', 'HEAD', cardinality=One)

class Shift(StructuredNode):
    ident = IntegerProperty(unique_index = True)
    workers = RelationshipFrom('Person', 'WORKER')
    chief = RelationshipFrom('Person', 'CHIEF', cardinality=One)

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
