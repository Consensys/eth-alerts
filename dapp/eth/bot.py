from utils import Singleton
from . import models
from events.models import Alert
from decoder import Decoder
from json import loads
from datetime import datetime
from django.utils import timezone
from web3 import Web3, HTTPProvider
from django.conf import settings


class Bot(Singleton):

    def __init__(self):
        super(Bot, self).__init__()
        self.decoder = Decoder()
        self.web3 = Web3(HTTPProvider(settings.ETHEREUM_NODE_URL))

    last_abi_datetime = datetime.fromtimestamp(0, timezone.get_current_timezone())
    decoder = None

    def next_block(self):
        return models.Daemon.get_solo().block_number

    def increase_block(self):
        daemon = models.Daemon.get_solo()
        daemon.block_number += 1
        daemon.save()

    def update_abis(self):
        now = timezone.now()
        since = self.last_abi_datetime
        alerts = Alert.objects.filter(created__gte=since)
        added = 0
        for alert in alerts:
            added += self.decoder.add_abi(loads(alert.abi))
        self.last_abi_datetime = now
        return added

    def get_next_logs(self):
        block = self.web3.eth.getBlock(self.next_block())
        logs = []
        for tx in block[u'transactions']:
            receipt = self.web3.eth.getTransactionReceipt(tx)
            if receipt.get('logs'):
                logs.extend(receipt[u'logs'])
        return self.decoder.decode_logs(logs)

    def execute(self):

        # update decoder with last abi's
        self.update_abis()

        # get block and decode logs
        try:
            logs = self.get_next_logs()
            # If decoded, add to the correct user collection in case of a valid event

            # get contract from log address (can be many)

            # If contract match, get event names

            # If event name filter, discard other events

            # Get event property, if event property, discard unmatched values

            # group events by contract

            # add to send mail

            # increase block number

        except ValueError:
            # Block not mined yet, so, continue execution
            pass