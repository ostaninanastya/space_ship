import sys, os
from datetime import datetime

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
        
        self.attack_angle %= 360
        self.direction_angle %= 360