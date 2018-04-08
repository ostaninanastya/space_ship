import graphene

class ControlActionMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()
    
    macaddress = graphene.String()
    username = graphene.String()
    userid = graphene.String()

    command = graphene.String()
    params = graphene.String()
    result = graphene.String()