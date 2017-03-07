from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel


class User(TimeStampedModel):
    """
    User class
    """
    email = models.TextField(unique=True)
    authentication_code = models.TextField()


class Alert(TimeStampedModel):
    """
    Alert Class
    """
    class Meta:
        unique_together = ('user', 'contract')

    user = models.ForeignKey(User)
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
    event = models.ForeignKey(Event, related_name='values', on_delete=models.CASCADE)