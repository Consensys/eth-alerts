# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from dapp.contracts import factories
from contracts.models import Contract
import simplejson


class TestContract(TestCase):

    def test_create(self):
        contract = factories.ContractFactory()
        self.assertIsNotNone(contract.pk)
        self.assertEquals(Contract.objects.get(pk=contract.id).address, contract.address)

    def test_update(self):
        contract = factories.ContractFactory()
        self.assertEquals(Contract.objects.get(pk=contract.id).address, contract.address)
        contract.address = '0x0'
        contract.save()
        check_contract = Contract.objects.get(pk=contract.id)
        self.assertEquals(contract.address, check_contract.address)



