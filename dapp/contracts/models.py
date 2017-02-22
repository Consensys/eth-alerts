from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel


class Contract(TimeStampedModel):
    """
    Contract Class
    """
    address = models.TextField()
