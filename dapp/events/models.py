from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel
from contracts.models import Contract


class EventName(TimeStampedModel):
    """
    Event Name Class
    """
    name = models.TextField()


class Email(TimeStampedModel):
    email = models.TextField()


class Alert(TimeStampedModel):
    """
    Alert Class
    """
    abi = models.TextField()
    email = models.ForeignKey(Email)
    is_confirmed = models.BooleanField()
    confirmation_key = models.TextField()
    delete_key = models.TextField()


class Event(TimeStampedModel):
    """
    Event Class
    """
    name = models.ForeignKey(EventName, blank=True, null=True)
    contract = models.ForeignKey(Contract)
    alert = models.ForeignKey(Alert, related_name='events')


class EventValue(TimeStampedModel):
    """
    Event Value Class
    """
    property = models.TextField()
    value = models.TextField()
    event = models.ForeignKey(Event, related_name='values')