# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from simplejson import dumps, loads
from events.models import Alert
from django.core import mail

class TestAlertView(APITestCase):

    def test_create(self):

        count_before = Alert.objects.all().count()
        num_emails_before = len(mail.outbox)
        data = {
            "contract": "contractAddress",
            "abi": [{'test': 'ok'}],
            "events": {
                "eventName": {
                    "eventPropertyName": "eventPropertyValue"
                }
            },
            "email": "giacomo.licari@gmail.com"
        }

        r = self.client.post(reverse('api:alert'), data=dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, r.status_code)

        count_after = alerts = Alert.objects.all().count()
        num_emails_ater = len(mail.outbox)

        # Check if the alert has been created
        self.assertEquals(count_after, count_before+1)
        # check if the email was sent
        self.assertEquals(num_emails_ater, num_emails_before+1)
        # Check if email context is filled
        self.assertEquals(mail.outbox[0].__dict__['context'].get('alert').abi, data.get('abi'))

    def test_create_fail(self):

        count_before = Alert.objects.all().count()
        num_emails_before = len(mail.outbox)
        data = {
            "contract": "contractAddress",
            "abi": [], # empty list fails as well as Null params
            "events": {
                "eventName": {
                    "eventPropertyName": "eventPropertyValue"
                }
            },
            "email": "giacomo.licari@gmail.com"
        }

        r = self.client.post(reverse('api:alert'), data=dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

        count_after = alerts = Alert.objects.all().count()
        num_emails_ater = len(mail.outbox)

        self.assertEquals(count_after, count_before)
        self.assertEquals(num_emails_ater, num_emails_before)



