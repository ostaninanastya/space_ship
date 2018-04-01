import sys, os
from datetime import datetime
import math

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

class Position(Model):
    time = columns.DateTime(required = True, primary_key = True)

    x = columns.Double(required = True, primary_key = True)
    y = columns.Double(required = True, primary_key = True)
    z = columns.Double(required = True, primary_key = True)

    speed = columns.Double(required = True, primary_key = True)
    attack_angle = columns.Double(required = True, primary_key = True)
    direction_angle = columns.Double(required = True, primary_key = True)

    def validate(self):
        super(Position, self).validate()

        self.attack_angle -= math.floor(self.attack_angle / (2 * math.pi)) * 2 * math.pi
        self.direction_angle -= math.floor(self.direction_angle / (2 * math.pi)) * 2 * math.pi