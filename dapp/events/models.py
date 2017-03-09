from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel


class DApp(TimeStampedModel):
    """
    DApp class
    """
    class Meta:
        unique_together = ('name', 'authentication_code')

    name = models.TextField()
    authentication_code = models.TextField()


class User(TimeStampedModel):
    """
    User class
    """
    email = models.TextField(unique=True)
    dapps = models.ManyToManyField(DApp)


class Alert(TimeStampedModel):
    """
    Alert Class
    """
    class Meta:
        unique_together = ('dapp', 'contract')

    dapp = models.ForeignKey(DApp, on_delete=models.DO_NOTHING)
    abi = models.TextField()
    contract = models.TextField()


class Event(TimeStampedModel):
    """
    Event Class
    """
    name = models.TextField()
    alert = models.ForeignKey(Alert, related_name='events')


class EventValue(TimeStampedModel):
    """
    Event Value Class
    """
    property = models.TextField()
    value = models.TextField()
    event = models.ForeignKey(Event, related_name='event_values', on_delete=models.CASCADE)