from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from app.decorators import jwt_auth
from app.gql.backends import GraphQLCustomCoreBackend

urlpatterns = [
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path(
        'graphql/',
        jwt_auth(
            csrf_exempt(
                GraphQLView.as_view(
                    graphiql=True, backend=GraphQLCustomCoreBackend()
                )
            )
        ),
        name='gql'
    )
]
