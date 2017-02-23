import factory
from faker import Factory as FakerFactory
from dapp.contracts.factories import ContractFactory
from events import models
import random
import hashlib

faker = FakerFactory.create()
randomSHA256 = lambda:hashlib.sha256(str(random.random())).hexdigest()


class EventNameFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.EventName

    name = faker.name()


class EmailFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Email

    email = faker.email()


class AlertFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Alert

    email = factory.SubFactory(EmailFactory)
    #event = factory.SubFactory(EventFactory)
    #name = faker.name()
    is_confirmed = True
    confirmation_key = randomSHA256()
    delete_key = randomSHA256()

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

    name = factory.SubFactory(EventNameFactory)
    contract = factory.SubFactory(ContractFactory)
    alert = factory.SubFactory(AlertFactory)


class EventValueFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.EventValue

    property = faker.name()
    value = faker.name()
    event = factory.SubFactory(EventFactory)
