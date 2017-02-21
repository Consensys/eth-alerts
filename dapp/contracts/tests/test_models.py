# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from dapp.contracts import factories
from contracts.models import Contract
import simplejson


class TestContract(TestCase):

    factory = None

    def setUp(self):
        TestContract.factory = factories.ContractFactory()

    def test_create(self):
        contract = Contract()
        contract.address = TestContract.factory.address
        contract.abi = simplejson.loads(TestContract.factory.abi)
        contract.save()

        self.assertIsNotNone(contract)
        self.assertEquals(TestContract.factory.address, contract.address)
        self.assertEquals(Contract.objects.get(pk=contract.id).address, contract.address)

    def test_update(self):
        contract = Contract()
        contract.address = TestContract.factory.address
        contract.abi = simplejson.loads(TestContract.factory.abi)
        contract.save()

        update_contract = Contract.objects.get(pk=contract.id)
        update_contract.address = '0x0'
        update_contract.save()

        check_contract = Contract.objects.get(pk=contract.id)
        self.assertEquals(update_contract.address, check_contract.address)



