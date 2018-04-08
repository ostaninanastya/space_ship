import graphene

class PositionMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()

    x = graphene.Float()
    y = graphene.Float()
    z = graphene.Float()

    speed = graphene.Float()
    attackangle = graphene.Float()
    directionangle = graphene.Float()