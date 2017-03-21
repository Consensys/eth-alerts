import factory
from faker import Factory as FakerFactory
from dapp.events.factories import UserFactory
from api.constants import AUTH_CODE_HEADER

faker = FakerFactory.create()


class Model(object):

    def __init__(self, abi, deletion_data, creation_data, signup_data, callback, user):
        self.abi = abi
        self.deletion_data = deletion_data
        self.creation_data = creation_data
        self.signup_data = signup_data
        self.callback = callback
        self.user = user


class APIFactory(factory.Factory):

    class Meta:
        model = Model

    callback = 'https://wallet.gnosis.pm/#/signup?' + AUTH_CODE_HEADER + '={%auth-code%}'

    @factory.LazyAttribute
    def user(self):
        return UserFactory()

    @factory.LazyAttribute
    def abi(self):
        data = '[{"inputs": [{"type": "address", "name": ""}], "constant": true, "name": "isInstantiation",' \
                   '"payable": false, "outputs": [{"type": "bool", "name": ""}], "type": "function"},' \
                   '{"inputs": [{"type": "address[]", "name": "_owners"}, {"type": "uint256", "name": "_required"},' \
                   '{"type": "uint256", "name": "_dailyLimit"}], "constant": false, "name": "create", "payable": false,' \
                   '"outputs": [{"type": "address", "name": "wallet"}], "type": "function"},' \
                   '{"inputs": [{"type": "address", "name": ""}, {"type": "uint256", "name": ""}],' \
                   '"constant": true, "name": "instantiations", "payable": false, "outputs":' \
                   '[{"type": "address", "name": ""}], "type": "function"}, {"inputs": [{"type":' \
                   '"address", "name": "creator"}], "constant": true, "name": "getInstantiationCount",' \
                   '"payable": false, "outputs": [{"type": "uint256", "name": ""}], "type": "function"},' \
                   '{"inputs": [{"indexed": false, "type": "address", "name": "sender"}, {"indexed": false,' \
                   '"type": "address", "name": "instantiation"}], "type": "event", "name": "ContractInstantiation",' \
                   '"anonymous": false}]'

        return data

    @factory.LazyAttribute
    def signup_data(self):
        data = dict(email=self.user.email, callback=self.callback, name=faker.name())
        return data

    @factory.LazyAttribute
    def creation_data(self):
        data = dict(abi=self.abi)

        data["contract"] = "0xd79426bcee5b46fde413ededeb38364b3e666097"
        data["email"] = faker.email()
        data["events"] = {
            "eventName1": {
                "eventPropertyName1_1": "eventPropertyValue1_1",
                "eventPropertyName1_2": "eventPropertyValue1_2"
            },
            "eventName2": {
                "eventPropertyName2_1": "eventPropertyValue2_1",
                "eventPropertyName2_2": "eventPropertyValue2_2"
            },
        }

        return data

    @factory.LazyAttribute
    def deletion_data(self):
        data = {
            "address": "0xd79426bcee5b46fde413ededeb38364b3e666097",
            "eventName": "eventName"
        }

        return data