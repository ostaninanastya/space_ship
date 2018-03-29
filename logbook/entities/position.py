import sys

from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import Memory

sys.path.append('entities/field_types')

class Position(Model):
	
	time = DateTimeField()
	
	x = Float64Field()
	y = Float64Field()
	z = Float64Field()

	speed = Float64Field()
	atack_angle = Float64Field()
	direction_angle = Float64Field()

	engine = Memory()