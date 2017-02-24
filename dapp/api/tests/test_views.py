# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from simplejson import dumps, loads
from events.models import Alert
from django.core import mail
from api.factories import APIFactory

class TestAlertView(APITestCase):

    def setUp(self):
        self.factory = APIFactory()

    def test_create(self):

        count_before = Alert.objects.all().count()
        num_emails_before = len(mail.outbox)
        data = self.factory.creation_data

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

        data = self.factory.creation_data
        data['abi'] = []

        r = self.client.post(reverse('api:alert'), data=dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

        count_after = alerts = Alert.objects.all().count()
        num_emails_ater = len(mail.outbox)

        self.assertEquals(count_after, count_before)
        self.assertEquals(num_emails_ater, num_emails_before)

    def test_confirm_creation(self):

        # Creation
        data = self.factory.creation_data
        creation_response = self.client.post(reverse('api:alert'), data=dumps(data), content_type='application/json')
        # Confirmation
        url = (reverse('api:alert-confirm', kwargs={'confirmation_key':creation_response.data['confirmation_key']}))
        confirmation_response = self.client.get(url, content_type='application/json')

        self.assertEqual(0, Alert.objects.filter(confirmation_key=creation_response.data['confirmation_key']).count())

    def test_delete_send_email_and_confirm(self):

        delete_data = self.factory.deletion_data
        create_data = self.factory.creation_data

        r_create = self.client.post(reverse('api:alert'), data=dumps(create_data), content_type='application/json')
        r_delete = self.client.delete(reverse('api:alert-delete'), data=dumps(delete_data), content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, r_delete.status_code)

        self.assertIsInstance(mail.outbox[0].__dict__['context'].get('alert'), Alert)
        delete_key = mail.outbox[0].__dict__['context'].get('alert').delete_key

        url = (reverse('api:alert-delete-confirm', kwargs={'delete_key': delete_key}))
        deletion_response = self.client.get(url, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, deletion_response.status_code)
        with self.assertRaises(Alert.DoesNotExist):
            Alert.DoesNotExist, Alert.objects.get(delete_key=delete_key)







