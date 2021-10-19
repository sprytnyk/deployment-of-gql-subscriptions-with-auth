from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from app.gql.consumers import CustomGraphqlSubscriptionConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path(
            'graphql/',
            CustomGraphqlSubscriptionConsumer
        )
    ]),
})
