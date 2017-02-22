# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from dapp.contracts import factories
from contracts import serializers
from contracts.models import Contract
import simplejson


class TestContractSerializer(TestCase):

    def test_contract_serializer(self):

        json_contract = '{"address":"0xd79426bcee5b46fde413ededeb38364b3e666097"}'

        # Instantiate the Factory
        contract = factories.ContractFactory()
        serialized_contract = serializers.ContractSerializer(contract)

        # Check serialization works
        self.assertEquals(simplejson.loads(json_contract)['address'], serialized_contract.data.get('address'))

