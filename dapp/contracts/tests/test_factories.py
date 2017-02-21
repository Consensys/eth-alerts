from django.test import TestCase
from dapp.contracts import factories


class TestContract(TestCase):

    def test_abi(self):
        contract = factories.ContractFactory()
        self.assertJSONEqual(contract.abi, '[{"inputs": [{"type": "uint256", "name": ""}], "constant": true}]')


    def test_contract(self):
        contract = factories.ContractFactory()
        contract.address = '0x0'
        self.assertEquals(contract.address, '0x0')

