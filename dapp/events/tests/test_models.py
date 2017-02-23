# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from events.models import (EventName, EventValue, Event, Email, Alert)
from contracts.models import Contract
from dapp.contracts.factories import ContractFactory
from dapp.events.factories import (EventNameFactory, EventFactory, EventValueFactory, EmailFactory)
import random
import hashlib


class TestEvent(TestCase):

    def test_create_event_name(self):
        event_name = EventNameFactory()
        event = EventName.objects.get(name=event_name.name)
        self.assertEquals(event.name, event_name.name)
        self.assertRaises(EventName.DoesNotExist, EventName.objects.get, name='Test2')

    def test_create_event(self):
        contract = ContractFactory()
        event_name = EventNameFactory()
        event = EventFactory()

        check_event = Event.objects.get(pk=event.id)
        self.assertEquals(check_event.name.name, event_name.name)
        self.assertEquals(check_event.contract.address, contract.address)

        event_value = EventValueFactory()
        check_event_value = EventValue.objects.get(event__id=event_value.event.id)
        self.assertEquals(check_event_value.property, event_value.property)

    def test_create_alert(self):
        contract = ContractFactory()
        event_name = EventNameFactory()
        event = EventFactory()
        event_value = EventValueFactory()
        email = EmailFactory()

        alert = Alert()
        alert.email = email
        alert.event = event
        alert.is_confirmed = False
        alert.confirmation_key = hashlib.sha256(str(random.random())).hexdigest()
        alert.save()

        check_alert = Alert.objects.get(pk = alert.id)
        self.assertEquals(check_alert.email.email, email.email)

        check_alert.is_confirmed = True
        check_alert.save()
        self.assertTrue(check_alert.is_confirmed)


