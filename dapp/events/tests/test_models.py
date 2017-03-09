# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from events.models import (User, DApp, EventValue, Event, Alert)
from dapp.events.factories import (DAppFactory, UserFactory, EventFactory, EventValueFactory, AlertFactory)
from django.db import IntegrityError
import random
import hashlib


class TestEvent(TestCase):

    def test_create_dapp(self):
        dapp = DAppFactory()
        dapp_obj = DApp.objects.get(name=dapp.name)
        self.assertEquals(dapp.name, dapp_obj.name)
        self.assertEquals(dapp.authentication_code, dapp_obj.authentication_code)
        self.assertRaises(DApp.DoesNotExist, DApp.objects.get, name='giacomo_fake_name')

        with self.assertRaises(IntegrityError): # duplicate key error
            dapp_duplicate = DApp()
            dapp_duplicate.user = dapp_obj.user
            dapp_duplicate.authentication_code = dapp_obj.authentication_code
            dapp_duplicate.name = dapp_obj.name
            dapp_duplicate.save()

    def test_create_user(self):
        dapp = DAppFactory()
        self.assertRaises(User.DoesNotExist, User.objects.get, email='test.giacomo@gmail.com')

    def test_create_alert_event(self):
        event = EventFactory()
        event_obj = Event.objects.get(alert=event.alert.id)
        self.assertEquals(event.name, event_obj.name)
        self.assertEquals(event.alert.contract, event_obj.alert.contract)
        self.assertEquals(event.alert.dapp.authentication_code, event_obj.alert.dapp.authentication_code)

        success_alert = Alert()
        success_alert.dapp = event.alert.dapp
        success_alert.abi = event.alert.abi
        success_alert.contract = "0x01234567"
        success_alert.save()

        # create duplicates
        fail_alert = Alert()
        fail_alert.dapp = event.alert.dapp
        fail_alert.abi = event.alert.abi
        fail_alert.contract = event.alert.contract

        with self.assertRaises(IntegrityError):
            fail_alert.save()