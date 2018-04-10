import sys, os

import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

class PositionMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()

    x = graphene.Float()
    y = graphene.Float()
    z = graphene.Float()

    speed = graphene.Float()
    attackangle = graphene.Float()
    directionangle = graphene.Float()

    @staticmethod
    def init_scalar(item):
    	return PositionMapper(date = date_to_str(item.date),
                       time = time_to_str(item.time),
                       x = item.x,
                       y = item.y,
                       z = item.z,
                       speed = item.speed,
                       attackangle = item.attack_angle,
                       directionangle = item.direction_angle)