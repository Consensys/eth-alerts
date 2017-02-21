from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel
from contracts.models import Contract

# Create your models here.


class EventName(TimeStampedModel):
    """
    Event Name Class
    """
    name = models.TextField()


class Event(TimeStampedModel):
    """
    Base Event Class
    """
    name = models.ForeignKey(EventName, blank=True, null=True)
    #values = models.OneToMany(EventValue)
    contract = models.ForeignKey(Contract)


class EventValue(TimeStampedModel):
    """
    Event Value Class
    """
    property = models.TextField()
    value = models.TextField()
    event = models.ForeignKey(Event)


class Email(TimeStampedModel):
    email = models.TextField()


class Alert(TimeStampedModel):
    email = models.ForeignKey(Email)
    event = models.ForeignKey(Event)
    name = models.TextField()
    is_confirmed = models.BooleanField()
    confirmation_key = models.IntegerField()