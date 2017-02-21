# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from events.models import (EventName, EventValue, Event, Email, Alert)
from contracts.models import Contract
from dapp.contracts.factories import ContractFactory
from dapp.events.factories import (EventNameFactory, EventFactory, EventValueFactory, EmailFactory)
import uuid


class TestEvent(TestCase):

    def test_create_event_name(self):
        factory = EventNameFactory()
        factory.save()

        event = EventName.objects.get(name=factory.name)
        self.assertEquals(event.name, factory.name)
        self.assertRaises(EventName.DoesNotExist, EventName.objects.get, name='Test2')

    def test_create_event(self):
        contract = ContractFactory()
        contract.save()

        event_name = EventNameFactory()
        event_name.save()

        event = EventFactory()
        event.save()

        check_event = Event.objects.get(pk=event.id)
        self.assertEquals(check_event.name.name, event_name.name)
        self.assertEquals(check_event.contract.address, contract.address)

        event_value = EventValueFactory()
        event_value.save()

        check_event_value = EventValue.objects.get(event__id=event_value.event.id)
        self.assertEquals(check_event_value.property, event_value.property)

    def test_create_alert(self):

        contract = ContractFactory()
        contract.save()

        event_name = EventNameFactory()
        event_name.save()

        event = EventFactory()
        event.save()

        event_value = EventValueFactory()
        event_value.save()

        email = EmailFactory()
        email.save()

        alert = Alert()
        alert.email = email
        alert.event = event
        alert.is_confirmed = False
        alert.confirmation_key = uuid.uuid4().hex
        alert.save()

        check_alert = Alert.objects.get(pk = alert.id)
        self.assertEquals(check_alert.email.email, email.email)

        check_alert.is_confirmed = True
        check_alert.save()
        self.assertTrue(check_alert.is_confirmed)


