from django.test import TestCase
from dapp.contracts import factories


class TestContract(TestCase):

    def test_contract(self):
        contract = factories.ContractFactory()
        contract.address = '0x0'
        self.assertEquals(contract.address, '0x0')

