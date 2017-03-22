import factory
from faker import Factory as FakerFactory
from events import models
import random
import hashlib

faker = FakerFactory.create()


def randomSHA256():
    return hashlib.sha256(str(random.random())).hexdigest()


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.User

    email = factory.Sequence(lambda n: faker.email())


class DAppFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.DApp

    name = factory.Sequence(lambda n: faker.name())
    authentication_code = factory.Sequence(lambda n: randomSHA256())
    user = factory.SubFactory(UserFactory)


class AlertFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Alert

    dapp = factory.SubFactory(DAppFactory)
    contract = factory.Sequence(lambda n: '0x{:040d}'.format(n))

    @factory.LazyAttribute
    def abi(self):
        abi_json = '[{"inputs": [{"type": "address", "name": ""}], "constant": true, "name": "isInstantiation",' \
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

        return abi_json


class EventFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Event

    name = faker.name()
    # alert = factory.SubFactory(AlertFactory)

    @factory.LazyAttribute
    def alert(self):
        return AlertFactory()


class EventValueFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.EventValue

    property = faker.name()
    value = faker.name()
    event = factory.SubFactory(EventFactory)
