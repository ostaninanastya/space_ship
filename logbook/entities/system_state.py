import sys

from enum import Enum

from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import Memory

sys.path.append('entities/field_types')

SystemStatuses = Enum('SystemStatuses', 'working fail being_fixed testing')

class SystemState(Model):
	
	time = DateTimeField()
	
	name = StringField()
	id = Int32Field()
	status = Enum8Field(SystemStatuses)

	engine = Memory()