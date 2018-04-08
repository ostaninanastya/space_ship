import graphene

class SystemTestMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()
    
    system = graphene.String()
    systemid = graphene.String()
    result = graphene.Int()