# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from models import (DApp, User, EventValue, Event, Alert)
import simplejson


class EventValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventValue
        fields = ('property', 'value')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            'name',
            'values',
            'alert'
        )

    values = EventValueSerializer(many=True)


class DAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = DApp
        fields = ('name', 'authentication_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'dapps')

    dapps = DAppSerializer(many=True)


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = (
            'dapp',
            # 'events',
            'abi',
            'contract'
        )

    dapp = DAppSerializer()

    def validate_abi(self, value):
        try:
            json_data = simplejson.loads(value)
        except:
            raise serializers.ValidationError('not valid input data')

        if not isinstance(json_data, list):
            raise serializers.ValidationError('field abi must be a JSON Array')

        return value