# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from events.models import (User, EventValue, Event, Alert)
from dapp.events.factories import (UserFactory, EventFactory, EventValueFactory, AlertFactory)
from django.db import IntegrityError
import random
import hashlib


class TestEvent(TestCase):

    def test_create_user(self):
        user = UserFactory()
        user_obj = User.objects.get(email=user.email)
        self.assertEquals(user.authentication_code, user_obj.authentication_code)
        self.assertRaises(User.DoesNotExist, User.objects.get, email='test.giacomo@gmail.com')

    def test_create_alert_event(self):
        event = EventFactory()
        event_obj = Event.objects.get(alert=event.alert.id)
        self.assertEquals(event.name, event_obj.name)
        self.assertEquals(event.alert.contract, event_obj.alert.contract)

        success_alert = Alert()
        success_alert.user = event.alert.user
        success_alert.abi = event.alert.abi
        success_alert.contract = "0x01234567"
        success_alert.save()

        # create duplicates
        fail_alert = Alert()
        fail_alert.user = event.alert.user
        fail_alert.abi = event.alert.abi
        fail_alert.contract = event.alert.contract

        with self.assertRaises(IntegrityError):
            fail_alert.save()