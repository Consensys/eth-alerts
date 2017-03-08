# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from dapp.events import factories
from events import serializers


class TestSerializers(TestCase):

    def test_user_serializer(self):
        dapp = factories.DAppFactory()
        user = factories.UserFactory()
        user.dapps.add(dapp)
        user.save()

        serialized_user = serializers.UserSerializer(user)
        self.assertIsNotNone(serialized_user)
        self.assertEquals(serialized_user.data.get('email'), user.email)
        self.assertEquals(serialized_user.data.get('dapps')[0].get('authentication_code'), user.dapps.all()[0].authentication_code)

        dapp_dict = {'name': None, 'authentication_code': dapp.authentication_code}
        user_dict = {'email': None}

        serialized_dapp_fail = serializers.DAppSerializer(data=dapp_dict)
        serialized_user_fail = serializers.UserSerializer(data=user_dict)
        self.assertFalse(serialized_dapp_fail.is_valid())
        self.assertFalse(serialized_user_fail.is_valid())

        dapp_dict['name'] = 'testname'
        user_dict['email'] = 'anotheremail@test.com'
        user_dict['dapps'] = [dapp_dict]

        serialized_dapp_success = serializers.DAppSerializer(data=dapp_dict)
        serialized_user_success = serializers.UserSerializer(data=user_dict)

        self.assertTrue(serialized_dapp_success.is_valid())
        self.assertTrue(serialized_user_success.is_valid())

    def test_event_serializer(self):
        event_value = factories.EventValueFactory()
        event = event_value.event
        serialized_event = serializers.EventSerializer(event)
        self.assertEquals(serialized_event.data.get('alert'), event.alert.id)
        self.assertEquals(event_value.event.name, serialized_event.data.get('name'))

    def test_alert_serializer(self):
        alert = factories.AlertFactory()
        serialized_alert = serializers.AlertSerializer(alert)
        self.assertEquals(serialized_alert.data.get('contract'), alert.contract)
        self.assertIsNotNone(serialized_alert.data.get('dapp').get('authentication_code'))
        self.assertEquals(serialized_alert.data.get('dapp').get('authentication_code'), alert.dapp.authentication_code)

        alert_dict = {
            'dapp': {
                'name': 'testname',
                'authentication_code': alert.dapp.authentication_code
            },
            'abi': alert.abi,
            'contract': alert.contract
        }

        self.assertTrue(serializers.AlertSerializer(data=alert_dict).is_valid())
        alert_dict['contract'] = None
        self.assertFalse(serializers.AlertSerializer(data=alert_dict).is_valid())

