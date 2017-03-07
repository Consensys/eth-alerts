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

from django.db import IntegrityError


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

        user.__dict__['callback'] = validated_data.get('callback').replace('{}', '?auth-code=%s' % user.authentication_code)

        return user

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'callback': instance.callback
        }


class AlertAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = ('contract', 'abi') #'__all__'

    contract = serializers.CharField()
    abi = serializers.ListField()
    events = serializers.OrderedDict()

    def to_internal_value(self, data):

        filtered_data = {}

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
            filtered_data['contract'] = data.get('contract')
        else:
            raise serializers.ValidationError({
                'contract': 'This field is required.'
            })

        # Events
        if data.get('events'):
            filtered_data['events'] = []
            events = data.get('events')
            filtered_events = dict()

            for key,values in events.iteritems():
                # Event Name
                event_name = key
                filtered_events[event_name] = {}
                if values:
                    for innerkey, innervalues in values.iteritems():
                        filtered_events[event_name][innerkey] = innervalues

            filtered_data['events'] = filtered_events

        else:
            # filtered_data['events'] = None
            raise serializers.ValidationError({
                'events': 'This field is required.'
            })

        return filtered_data

    def create(self, validated_data):
        # Create the objects
        eventvalue_obj = None
        event_obj = None
        alert_obj = None

        try:
            alert_obj = Alert.objects.get(contract=validated_data.get('contract'))
        except Alert.DoesNotExist:
            alert_obj = Alert()
            alert_obj.abi = validated_data.get('abi')
            alert_obj.user = self.context['request'].user
            alert_obj.contract = validated_data.get('contract')
            alert_obj.save()

        if validated_data.get('events'):
            events_obj = Event.objects.filter(alert=alert_obj.id)
            events_obj.delete()

            for key in validated_data.get('events'):
                properties_dict = validated_data.get('events').get(key)
                event_obj = Event()
                event_obj.name = key
                event_obj.alert = alert_obj
                event_obj.save()

                for propertykey, propertyvalue in properties_dict.iteritems():
                    # Event Value object
                    eventvalue_obj = EventValue()
                    eventvalue_obj.property = propertykey
                    eventvalue_obj.value = propertyvalue
                    eventvalue_obj.event = event_obj
                    eventvalue_obj.save()

        return alert_obj

    def to_representation(self, instance):
        return {}


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