from django.db import models
from django.db.models.signals import post_delete, post_save
from graphene_subscriptions.signals import (
    post_delete_subscription,
    post_save_subscription
)


class Car(models.Model):
    make = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    variant = models.CharField(max_length=256)
    year = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.make} {self.model} {self.variant} {self.year}'


post_save.connect(
    post_save_subscription,
    sender=Car,
    dispatch_uid='car_post_save'
)
post_delete.connect(
    post_delete_subscription,
    sender=Car,
    dispatch_uid='car_post_delete'
)
