# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from simplejson import dumps, loads
from events.models import Alert
from django.core import mail
from api.factories import APIFactory
from events.factories import DAppFactory
from api.constants import DJANGO_AUTH_CODE_HEADER, AUTH_CODE_HEADER


class TestAlertView(APITestCase):

    def setUp(self):
        self.factory = APIFactory()
        self.signup_data = self.factory.signup_data
        signup_response = self.client.post(reverse('api:signup'), data=dumps(self.signup_data), content_type='application/json')
        self.assertEquals(signup_response.status_code, status.HTTP_201_CREATED)
        callback = signup_response.data.get('callback')
        self.assertIsNotNone(callback)
        matches = callback.split(AUTH_CODE_HEADER + '=')
        self.assertIsNotNone(matches)
        self.assertEqual(len(matches), 2)
        self.auth_code = callback.split(AUTH_CODE_HEADER + '=')[1]
        self.auth_header = dict()
        self.auth_header[DJANGO_AUTH_CODE_HEADER] = self.auth_code

    def test_signup(self):
        num_emails_before = len(mail.outbox)
        signup_data = self.factory.signup_data
        signup_response = self.client.post(
            reverse('api:signup'),
            data=dumps(signup_data),
            content_type='application/json'
        )
        self.assertEquals(signup_response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(signup_data.get('email'), signup_response.data.get('email'))
        self.assertIsNotNone(signup_data.get('callback'))

        self.signup_data = signup_response.data

        num_emails_after = len(mail.outbox)

        # check if the email was sent
        self.assertEquals(num_emails_after, num_emails_before+1)
        # Check if email context is filled
        self.assertIsNotNone(mail.outbox[0].__dict__['context'].get('callback'))

        signup_fails_data = signup_data.copy()
        signup_fails_data['email'] = None
        response_fails = self.client.post(reverse('api:signup'), data=dumps(signup_fails_data), content_type='application/json')
        self.assertEquals(response_fails.status_code, status.HTTP_400_BAD_REQUEST)

        signup_fails_data = signup_data.copy()
        signup_fails_data['email'] = 'email_not_valid'
        response_fails = self.client.post(reverse('api:signup'), data=dumps(signup_fails_data), content_type='application/json')
        self.assertEquals(response_fails.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_auth_code(self):
        data = self.factory.creation_data
        response = self.client.post(reverse('api:alert'), data=dumps(data), content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_update(self):
        count_before = Alert.objects.all().count()

        # Create alert and events
        create_data = self.factory.creation_data.copy()
        create_response = self.client.post(
            reverse('api:alert'),
            data=dumps(create_data),
            content_type='application/json',
            **self.auth_header
        )

        self.assertEqual(status.HTTP_201_CREATED, create_response.status_code)
        count_after = Alert.objects.all().count()

        # Check if the alert has been created
        self.assertEquals(count_after, count_before+1)

        # Test update
        update_data = create_data.copy()
        update_data['events'] = {create_data.get('events').items()[0][0]: create_data.get('events').items()[0][1]}
        update_response = self.client.post(
            reverse('api:alert'),
            data=dumps(update_data),
            content_type='application/json',
            **self.auth_header
        )

        self.assertEquals(status.HTTP_201_CREATED, update_response.status_code)
        self.assertEquals(1, Alert.objects.filter(dapp__authentication_code=self.auth_code)[0].events.count())

    def test_alert_delete(self):
        create_data = self.factory.creation_data.copy()

        create_response = self.client.post(
            reverse('api:alert'),
            data=dumps(create_data),
            content_type='application/json',
            **self.auth_header
        )

        create_data['events'] = None

        dapp = DAppFactory()

        fail_auth_header = self.auth_header.copy()
        fail_auth_header[DJANGO_AUTH_CODE_HEADER] = dapp.authentication_code

        delete_response_fails = self.client.post(
            reverse('api:alert'),
            data=dumps(create_data),
            content_type='application/json',
            **fail_auth_header
        )

        self.assertEquals(delete_response_fails.status_code, status.HTTP_401_UNAUTHORIZED)

        delete_response_success = self.client.delete(
            reverse('api:alert'),
            data=dumps(create_data),
            content_type='application/json',
            **self.auth_header
        )

        self.assertEquals(status.HTTP_200_OK, delete_response_success.status_code)

    def test_creat_no_values(self):
        # Create an Event with no values
        create_data =  self.factory.creation_data.copy()
        create_data['events'] = {'testEventName': None}

        create_response = self.client.post(
            reverse('api:alert'),
            data=dumps(create_data),
            content_type='application/json',
            **self.auth_header
        )

        self.assertEquals(status.HTTP_201_CREATED, create_response.status_code)

    def test_get_alert(self):
        create_data = self.factory.creation_data.copy()
        get_data = {'contract': create_data.get('contract')}

        create_response = self.client.post(
            reverse('api:alert'),
            data=dumps(create_data),
            content_type='application/json',
            **self.auth_header
        )

        get_response = self.client.get(
            reverse('api:alert'),
            get_data,
            content_type='application/json',
            **self.auth_header
        )

        self.assertEquals(status.HTTP_200_OK, get_response.status_code)
        for key in get_response.data:
            self.assertIn(key, get_response.data.keys())

        get_data['contract'] = '0x0'
        get_empty_response = self.client.get(reverse('api:alert'),
                                             get_data,
                                             content_type='application/json',
                                             **self.auth_header)

        self.assertEquals(status.HTTP_200_OK, get_empty_response.status_code)
        self.assertDictEqual(get_empty_response.data, {})


    """def test_create_fail(self):

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

    def test_confirm_fails(self):

        # Creation
        data = self.factory.creation_data
        creation_response = self.client.post(reverse('api:alert'), data=dumps(data), content_type='application/json')
        # Confirmation
        url = (reverse('api:alert-confirm', kwargs={'confirmation_key':False}))
        confirmation_response = self.client.get(url, content_type='application/json')
        self.assertEquals(confirmation_response.status_code, 400)

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

    def test_delete_fails(self):
        delete_data = self.factory.deletion_data
        create_data = self.factory.creation_data

        delete_data['address'] = None

        r_create = self.client.post(reverse('api:alert'), data=dumps(create_data), content_type='application/json')
        r_delete = self.client.delete(reverse('api:alert-delete'), data=dumps(delete_data), content_type='application/json')

        self.assertEquals(r_delete.status_code, 400)


    def test_get_alert_no_events(self):
        create_data = self.factory.creation_data.copy()
        create_data['events'] = {}
        get_data = {'email': create_data['email']}

        r_create = self.client.post(reverse('api:alert'), data=dumps(create_data), content_type='application/json')
        r_get = self.client.get(reverse('api:alert'), get_data, content_type='application/json')

        self.assertEquals(status.HTTP_200_OK, r_get.status_code)
        self.assertEquals(len(r_get.data[create_data['contract']]), 1)
        self.assertEquals(r_get.data[create_data['contract']][0]['values'], [])"""







