import graphene

from app.gql.subscriptions import CarSubscription


class Query(graphene.ObjectType):
    hi = graphene.String(default_value='Hi!')


class Subscription(CarSubscription):
    pass


schema = graphene.Schema(query=Query, subscription=Subscription)
