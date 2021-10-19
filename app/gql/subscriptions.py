import graphene
from graphene_django.types import DjangoObjectType
from graphene_subscriptions.events import UPDATED

from app.models import Car


class CarModelType(DjangoObjectType):
    class Meta:
        model = Car


class CarSubscription(graphene.ObjectType):
    car_model_updated = graphene.Field(CarModelType, pk=graphene.ID())

    def resolve_car_model_updated(self, info, pk):
        return (
            self.filter(
                lambda event:
                event.operation == UPDATED and
                isinstance(event.instance, Car) and
                event.instance.pk == int(pk)
            )
            .map(lambda event: event.instance)
        )
