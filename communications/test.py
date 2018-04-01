import os, sys
import configparser

from neomodel import StructuredNode, IntegerProperty, StringProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, config, One

sys.path.append('entities')

from department import Department
from operation import Operation
from person import Person
from requirement import Requirement
from shift import Shift

configp = configparser.ConfigParser()
configp.read('../databases.config')

NEO4J_DB_URL = os.environ.get('NEO4J_DB_URL') if os.environ.get('NEO4J_DB_URL') else configp['NEO4J']['host']
NEO4J_DB_PORT = int(os.environ.get('NEO4J_DB_PORT') if os.environ.get('NEO4J_DB_PORT') else configp['NEO4J']['port'])

USERNAME = os.environ.get('NEO4J_DB_USERNAME') if os.environ.get('NEO4J_DB_USERNAME') else configp['NEO4J']['username']
PASSWORD = os.environ.get('NEO4J_DB_PASSWORD') if os.environ.get('NEO4J_DB_PASSWORD') else configp['NEO4J']['password']

config.DATABASE_URL = 'bolt://' + USERNAME + ':' + PASSWORD + '@' + NEO4J_DB_URL + ':' + str(NEO4J_DB_PORT)


buzz = Person(ident = '5abfdba6ee6b7f5eec83a1ca').save() #id will be checked in mongo and saved as array of two ints
print(buzz.ident_hex) #show identifier as a hex string
'''
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
'''
