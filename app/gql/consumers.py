import json
from dataclasses import dataclass, field
from functools import partial
from typing import List, Optional, Union

from django.contrib.auth.models import AnonymousUser, User
from django.db import close_old_connections
from graphene_django.settings import graphene_settings
from graphene_subscriptions.consumers import (
    AttrDict,
    GraphqlSubscriptionConsumer,
    stream
)
from rx.core.anonymousobservable import AnonymousObservable

from app.utils import decode_jwt_token


@dataclass
class Result:
    """GQL result placeholder."""

    errors: List[str]
    data: dict = field(default_factory=dict)


def get_user(token: Optional[str]) -> Union[AnonymousUser, User]:
    """Returns an anonymous user or authenticated one by a provided token."""

    if data := decode_jwt_token(token):
        return User.objects.get(id=data['user_id'])
    else:
        return AnonymousUser()


class CustomGraphqlSubscriptionConsumer(GraphqlSubscriptionConsumer):
    def __init__(self, *args, **kwargs):
        self.user = None
        self.token = None

        super().__init__(*args, **kwargs)

    def __connection_init(self, payload: dict) -> None:
        if token := payload.get('Authorization'):
            self.token = token.split(' ')[-1]

        self.user = get_user(self.token)
        close_old_connections()

    def __connection_start(
            self, payload: dict
    ) -> Union[Result, AnonymousObservable]:
        if isinstance(self.user, AnonymousUser):
            error = {'Authorization': 'Token is invalid or not provided.'}
            return Result(errors=[json.dumps(error)])

        if not payload:
            error = {'Payload': 'No payload was provided.'}
            return Result(errors=[json.dumps(error)])

        context = AttrDict(self.scope)
        schema = graphene_settings.SCHEMA

        return schema.execute(
            payload['query'],
            operation_name=payload.get('operationName'),
            variables=payload.get('variables'),
            context=context,
            root=stream,
            allow_subscriptions=True,
        )

    def websocket_receive(self, message):
        request = json.loads(message['text'])
        payload_id = request.get('id')
        payload = request.get('payload')

        if request['type'] == 'connection_init':
            self.__connection_init(payload)

        elif request['type'] == 'start':
            result = self.__connection_start(payload)

            if hasattr(result, 'subscribe'):
                result.subscribe(partial(self._send_result, payload_id))
            else:
                self._send_result(payload_id, result)

        elif request['type'] == 'stop':
            pass
