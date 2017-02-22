# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from dapp.events import factories
from events import serializers


class TestEventSerializer(TestCase):

    def test_event_name_serializer(self):
        event_name = factories.EventNameFactory()
        serialized_object = serializers.EventNameSerializer(event_name)
        self.assertEquals(event_name.name, serialized_object.data.get('name'))

    def test_event_serializer(self):
        event = factories.EventFactory()
        event_value = factories.EventValueFactory()
        event_value.event = event

        event.save()
        event_value.save()

        serialized_event = serializers.EventSerializer(event)

        self.assertEquals(serialized_event.data.get('contract').get('address'), event.contract.address)
        self.assertEquals(event_value.event.name.name, serialized_event.data.get('name').get('name'))