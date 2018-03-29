import sys

from enum import Enum

from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import Memory

sys.path.append('entities/field_types')

SensorLocations = Enum('SensorLocations', 'top_edge left_side right_side bottom_edge laboratory internal_area semi_internal_area')
SensorEvent = Enum('SensorEvent', 'timeout request')
SensorValueName = Enum('SensorValueName', 'cold_dark_matter_concentration hot_dark_matter_concentration warm_dark_matter_concentration space_radiation')
SensorValueUnits = Enum('SensorValueUnits', 'CeV TeV eV keV')

class SensorData(Model):
	
	time = DateTimeField()
	
	source = StringField()
	location = Enum8Field(SensorLocations)
	event = Enum8Field(SensorEvent)
	value_name = Enum8Field(SensorValueName)
	value = Float64Field()
	units = Enum8Field(SensorValueUnits)

	engine = Memory()