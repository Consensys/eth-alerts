# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from events.models import (
    User,
    EventValue,
    Event,
    Alert
)
from events.serializers import (
    UserSerializer,
    EventValueSerializer,
    EventSerializer,
    AlertSerializer
)
from api.utils import get_SHA256


class SignupAPISerializer(serializers.Serializer):

    email = serializers.EmailField()
    callback = serializers.CharField()

    def create(self, validated_data):
        user = None
        try:
            user = User.objects.get(email=validated_data.get('email'))
        except User.DoesNotExist:
            user = User()
            user.email = validated_data.get('email')
            user.authentication_code = get_SHA256()
            user.save()

        user.__dict__['callback'] = validated_data.get('callback').replace('{}', '?authetication_code=%s' % user.authentication_code)

        return user

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'callback': instance.callback
        }




class AlertAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = '__all__'

    abi = serializers.ListField()
    # email = EmailSerializer()
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

        """try:
            contract_obj = Contract.objects.get(address=validated_data.get('contract').get('address'))
        except Contract.DoesNotExist:
            contract_obj = Contract.objects.create(**validated_data.get('contract'))

        email_obj = Email.objects.create(**validated_data.get('email'))

        alert_obj = Alert()
        alert_obj.abi = validated_data.get('abi')
        alert_obj.email = email_obj
        alert_obj.is_confirmed = False
        alert_obj.confirmation_key = get_SHA256()
        alert_obj.delete_key = get_SHA256()
        alert_obj.save()

        if validated_data.get('events'):
            for event in validated_data.get('events'):
                # EventName object
                try:
                    eventname_obj = EventName.objects.get(name=event.get('name').get('name'))
                except EventName.DoesNotExist:
                    eventname_obj = EventName.objects.create(**event.get('name'))


                try:
                    event_obj = Event.objects.get(contract=contract_obj, name=eventname_obj)
                except Event.DoesNotExist:
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
        else:
            event_obj = Event()
            event_obj.name = None
            event_obj.contract = contract_obj
            event_obj.alert = alert_obj
            event_obj.save()

        return alert_obj"""


class AlertDeleteAPISerializer(serializers.Serializer):

    class Meta:
        fields = ['address', 'eventName']

    address = serializers.CharField()
    eventName = serializers.CharField()

    def validate(self, attrs):
        if not attrs.get('address'):
            raise serializers.ValidationError({
                'address': 'This field is required.'
            })

        if not attrs.get('eventName'):
            raise serializers.ValidationError({
                'eventName': 'This field is required.'
            })

        return attrs