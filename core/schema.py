import graphene
import app.schema

class Query(app.schema.Query, graphene.ObjectType):
    ...


class Mutation(app.schema.Mutation, graphene.ObjectType):
    ...

schema = graphene.Schema(query=Query, mutation=Mutation)
