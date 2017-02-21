# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from models import Contract
import simplejson


class ContractSerializer(serializers.Serializer):

    class Meta:
        fields = [
            'address',
            'abi'
        ]

    address = serializers.CharField()
    abi = serializers.CharField()

    def validate(self, data):
        try:
            json_data = simplejson.loads(data)
        except:
            raise serializers.ValidationError('not valid input data')

        if json_data.get('address') is None:
            raise serializers.ValidationError('missing field address')

        if json_data.get('abi') is None:
            raise serializers.ValidationError('missing field abi')
        else:
            if not isinstance(json_data.get('abi'), list):
                raise serializers.ValidationError('field abi must be a JSON Array')


        # Check if contract exists
        contract = Contract.objects.get(address=json_data.get('address'))

        if contract is not None:
            raise serializers.ValidationError('Contract already exists')

        return data

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)

