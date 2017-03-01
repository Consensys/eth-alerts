import factory
from faker import Factory as FakerFactory
from dapp.contracts.models import Contract

faker = FakerFactory.create()


class ContractFactory(factory.DjangoModelFactory):

    class Meta:
        model = Contract

    address = "0xd79426bcee5b46fde413ededeb38364b3e666097"
