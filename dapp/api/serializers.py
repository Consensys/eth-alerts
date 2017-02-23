# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from contracts.models import Contract
from events.models import (
    EventName,
    EventValue,
    Event,
    Email,
    Alert
)
from events.serializers import (
    EmailSerializer,
    EventValueSerializer,
    EventNameSerializer,
    EventSerializer,
    AlertSerializer
)
from contracts.serializers import ContractSerializer

import hashlib
import random


class AlertAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = '__all__'

    # contract = ContractSerializer()
    abi = serializers.ListField()
    email = EmailSerializer()
    events = EventSerializer(many=True)

    def to_internal_value(self, data):

        filtered_data = {}

        # Email
        if data.get('email'):
            filtered_data['email'] = {'email' : data.get('email')}
        else:
           raise  serializers.ValidationError({
                'email': 'This field is required.'
            })

        # ABI
        if data.get('abi'):
            if not isinstance(data.get('abi'), list):
                raise serializers.ValidationError({
                    'abi': 'This field is required.'
                })

            filtered_data['abi'] = data.get('abi')
        else:
            raise serializers.ValidationError({
                'abi': 'This field is required.'
            })

        # Contract
        if data.get('contract'):
            filtered_data['contract'] = {'address' : data.get('contract')}
        else:
            raise serializers.ValidationError({
                'contract': 'This field is required.'
            })

        # Events
        if data.get('events'):
            filtered_data['events'] = []
            events = data.get('events')
            event = dict()
            event['contract'] = filtered_data.get('contract')
            event['values'] = []

            for k,v in events.iteritems():
                # Event Name
                event['name'] = {'name' : k}

                property_key = events[k].keys()[0]
                value= events[k][property_key]

                event['values'].append({
                    'property' : property_key,
                    'value' : value
                })

            filtered_data['events'].append(event)

        else:
            filtered_data['events'] = None

        return filtered_data

    def create(self, validated_data):
        # Create the objects
        contract_obj = None
        eventvalue_obj = None
        eventname_obj = None
        email_obj = None
        alert_obj = None

        contract_obj = Contract.objects.create(**validated_data.get('contract'))
        email_obj = Email.objects.create(**validated_data.get('email'))

        alert_obj = Alert()
        alert_obj.abi = validated_data.get('abi')
        alert_obj.email = email_obj
        alert_obj.is_confirmed = False
        alert_obj.confirmation_key = hashlib.sha256(str(random.random())).hexdigest()
        alert_obj.delete_key = hashlib.sha256(str(random.random())).hexdigest()
        alert_obj.save()


        for event in validated_data.get('events'):
            # EventName object
            eventname_obj = EventName.objects.create(**event.get('name'))
            # Event Object
            event_obj = Event()
            event_obj.name = eventname_obj
            event_obj.contract = contract_obj
            event_obj.alert = alert_obj
            event_obj.save()

            for value in event.get('values'):
                # Event Value object
                eventvalue_obj = EventValue()
                eventvalue_obj.property = value.get('property')
                eventvalue_obj.value = value.get('value')
                eventvalue_obj.event = event_obj
                eventvalue_obj.save()

        return alert_obj

