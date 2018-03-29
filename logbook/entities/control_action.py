import sys

from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import Memory

sys.path.append('entities/field_types')

class ControlAction(Model):
	
	time = DateTimeField()
	
	mac_address = StringField()
	user = StringField()
	command = StringField()
	params = StringField()
	result = StringField()

	engine = Memory()