import sys, os
import graphene

from sensor_mapper import SensorMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

class SensorDataMapper(graphene.ObjectType):

    date = graphene.String()
    time = graphene.String()

    sourceid = graphene.String()
    source = graphene.Field(SensorMapper)
    location = graphene.String()
    event = graphene.String()
    valuename = graphene.String()
    value = graphene.Float()
    units = graphene.String()

    def resolve_source(self, info):
        return SensorMapper(id = self.sourceid)