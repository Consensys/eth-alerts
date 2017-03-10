# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from events.models import (
    DApp,
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
from api.constants import AUTH_CODE_HEADER
import json


class SignupAPISerializer(serializers.Serializer):

    email = serializers.EmailField()
    callback = serializers.CharField()
    name = serializers.CharField() # dapp name

    def create(self, validated_data):
        dapp_obj = None
        user_obj = None

        try:
            user_obj = User.objects.get(email=validated_data.get('email'))
        except User.DoesNotExist:
            user_obj = User()
            user_obj.email = validated_data.get('email')
            user_obj.save()

        dapp_obj = DApp()
        dapp_obj.authentication_code = get_SHA256()
        dapp_obj.name = validated_data.get('name')
        dapp_obj.user = user_obj
        dapp_obj.save()

        user_obj.__dict__['callback'] = validated_data.get('callback').replace('{%' + AUTH_CODE_HEADER + '%}', '?%s=%s' % (
                                                                               AUTH_CODE_HEADER,
                                                                               dapp_obj.authentication_code)
                                                                            )

        return user_obj

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'callback': instance.callback
        }


class AlertAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = ('contract', 'abi')

    contract = serializers.CharField()
    abi = serializers.ListField()
    events = serializers.OrderedDict()

    def to_internal_value(self, data):

        filtered_data = {}

        # ABI
        if data.get('abi'):
            abi = None
            try:
                if not isinstance(json.loads(data.get('abi')), list):
                    raise serializers.ValidationError({
                        'abi': 'This field is required.'
                    })
            except Exception as e:
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

        return filtered_data

    def create(self, validated_data):
        # Create the objects
        eventvalue_obj = None
        event_obj = None
        alert_obj = None

        try:
            alert_obj = Alert.objects.get(
                dapp__authentication_code=self.context['request'].auth.authentication_code,
                contract=validated_data.get('contract')
            )
        except Alert.DoesNotExist:
            alert_obj = Alert()
            alert_obj.abi = validated_data.get('abi')
            alert_obj.dapp = self.context['request'].auth
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
        else:
            # Delete Alert when no Events in request body
            alert_obj.delete()

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