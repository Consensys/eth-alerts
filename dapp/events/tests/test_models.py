# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from events.models import (EventName, EventValue, Event, Email, Alert)
from contracts.models import Contract
from dapp.contracts import factories
import uuid


class TestEvent(TestCase):

    def test_create_event_name(self):
        event = EventName()
        event.name = 'Test1'
        event.save()

        e = EventName.objects.get(name='Test1')
        self.assertEquals(e.name, 'Test1')
        self.assertRaises(EventName.DoesNotExist, EventName.objects.get, name='Test2')

    def test_create_event(self):
        factory = factories.ContractFactory()

        contract = Contract()
        contract.address = factory.address
        contract.abi = factory.abi
        contract.save()

        event_name = EventName()
        event_name.name = 'TestEvent'
        event_name.save()

        event = Event()
        event.name = event_name
        event.contract = contract
        event.save()

        check_event = Event.objects.get(pk=event.id)
        self.assertEquals(check_event.name.name, event_name.name)
        self.assertEquals(check_event.contract.address, contract.address)

        event_value = EventValue()
        event_value.property = 'property'
        event_value.value = '1'
        event_value.event = event
        event_value.save()

        check_event_value = EventValue.objects.get(event__id=event.id)
        self.assertEquals(check_event_value.property, event_value.property)

    def test_create_alert(self):

        factory = factories.ContractFactory()

        contract = Contract()
        contract.address = factory.address
        contract.abi = factory.abi
        contract.save()

        event_name = EventName()
        event_name.name = 'TestEvent'
        event_name.save()

        event = Event()
        event.name = event_name
        event.contract = contract
        event.save()

        event_value = EventValue()
        event_value.property = 'property'
        event_value.value = '1'
        event_value.event = event
        event_value.save()

        email = Email()
        email.email = 'giacomo.licari@gmail.com'
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


