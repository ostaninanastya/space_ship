import graphene

class PersonMapper(graphene.ObjectType):
	name = graphene.String()

	id = graphene.String()