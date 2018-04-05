import sys, os
from datetime import datetime
import math

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

class Position(Model):
    date = columns.Date(required = True, partition_key = True)
    time = columns.Time(required = True, primary_key = True)

    x = columns.Double(required = True)
    y = columns.Double(required = True)
    z = columns.Double(required = True)

    speed = columns.Double(required = True)
    attack_angle = columns.Double(required = True)
    direction_angle = columns.Double(required = True)

    def validate(self):
        super(Position, self).validate()

        self.attack_angle = Position.validate_angle(self.attack_angle)
        self.direction_angle = Position.validate_angle(self.direction_angle)

    @staticmethod
    def validate_angle(angle):
        angle -= math.floor(angle / (2 * math.pi)) * 2 * math.pi
        return angle