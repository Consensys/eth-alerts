# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from models import (Event, Email, Alert)
from contracts.serializers import ContractSerializer
import simplejson


class EventNameSerializer(serializers.Serializer):

    class Meta:
        fields = [
            'name'
        ]

    name = serializers.CharField()

    def validate(self, attrs):
        return attrs


class EventValueSerializer(serializers.Serializer):

    class Meta:
        fields = []

    property = serializers.CharField()
    value = serializers.CharField()
    #event = EventSerializer()

    def validate(self, attrs):
        return attrs


class EventSerializer(serializers.Serializer):

    class Meta:
        fields = [
            'name',
            'contract',
            'event_values'
        ]

    name = EventNameSerializer()
    contract = ContractSerializer()
    values = EventValueSerializer(many=True)

    def validate(self, attrs):
        return attrs


class EmailSerializer(serializers.Serializer):

    class Meta:
        fields = [
            'email'
        ]

    email = serializers.CharField()

    def validate(self, attrs):
        return attrs



class AlertSerializer(serializers.Serializer):

    class Meta:
        fields = [
            'email',
            'event',
            'abi',
            'name',
            'is_confirmed',
            'confirmation_key',
            'delete_key'
        ]

    email = EmailSerializer()
    event = EventSerializer()
    abi = serializers.CharField()
    name = serializers.CharField()
    is_confirmed = serializers.BooleanField()
    confirmation_key = serializers.CharField()
    delete_key = serializers.CharField()

    def validate(self, attrs):
        try:
            json_data = simplejson.loads(attrs)
        except:
            raise serializers.ValidationError('not valid input data')

        if json_data.get('abi') is None:
            raise serializers.ValidationError('missing field abi')
        else:
            if not isinstance(json_data.get('abi'), list):
                raise serializers.ValidationError('field abi must be a JSON Array')


        return attrs