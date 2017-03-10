# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    """
    Event admin
    """


@admin.register(models.Alert)
class AlertAdmin(admin.ModelAdmin):
    """
    Alert admin
    """


@admin.register(models.EventValue)
class EventValuesAdmin(admin.ModelAdmin):
    """
    EventValue admin
    """


@admin.register(models.DApp)
class DappAdmin(admin.ModelAdmin):
    """
    Dapp admin
    """


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """
    User admin
    """