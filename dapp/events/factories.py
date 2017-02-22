import factory
from factory import fuzzy
from faker import Factory as FakerFactory
from dapp.contracts.factories import ContractFactory
from events import models

faker = FakerFactory.create()


class EventNameFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.EventName

    name = faker.name()


class EventFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Event

    name = factory.SubFactory(EventNameFactory)
    contract = factory.SubFactory(ContractFactory)


class EventValueFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.EventValue

    property = faker.name()
    value = faker.name()
    event = factory.SubFactory(EventFactory)


class EmailFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Email

    email = faker.email()


class AlertFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Alert

    email = factory.SubFactory(EmailFactory)
    event = factory.SubFactory(EventFactory)
    name = faker.name()
    is_confirmed = True
    confirmation_key = faker.name()
    delete_key = faker.name()

    @factory.LazyAttribute
    def abi(self):
        abi_json = '[{"inputs": [{"type": "uint256", "name": ""}], "constant": true}]'
        return abi_json
