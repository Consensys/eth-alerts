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
