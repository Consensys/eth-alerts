# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from models import Contract
import simplejson


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ('address',)

    #address = serializers.CharField()

    def validate(self, data):

        """json_data = None
        try:
            json_data = simplejson.loads(data)
        except:
            raise serializers.ValidationError('not valid input data')"""

        if data.get('address') is None:
            raise serializers.ValidationError('missing field address')

        return data

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)

