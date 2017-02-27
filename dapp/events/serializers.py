# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from models import (EventName, EventValue, Event, Email, Alert)
from contracts.serializers import ContractSerializer
import simplejson


class EventNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventName
        fields = ('name',)


class EventValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventValue
        fields = ('property', 'value')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            'name',
            'contract',
            'values'
        )

    name = EventNameSerializer()
    contract = ContractSerializer()
    values = EventValueSerializer(many=True)


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = ('email',)


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = (
            'email',
            'events',
            'abi',
            'is_confirmed',
            'confirmation_key',
            'delete_key'
        )

    email = EmailSerializer()
    events = EventSerializer(many=True)

    def validate_abi(self, value):
        try:
            json_data = simplejson.loads(value)
        except:
            raise serializers.ValidationError('not valid input data')

        if not isinstance(json_data, list):
            raise serializers.ValidationError('field abi must be a JSON Array')

        return value