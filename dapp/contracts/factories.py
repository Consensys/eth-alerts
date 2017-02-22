import factory
from factory import fuzzy
from faker import Factory as FakerFactory
from contracts import models

faker = FakerFactory.create()


class ContractFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Contract

    address = "0xd79426bcee5b46fde413ededeb38364b3e666097"
