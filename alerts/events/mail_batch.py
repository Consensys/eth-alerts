from utils import Singleton
from api.utils import send_email
from django.urls import reverse
from django.conf import settings
from django.apps import apps


class MailBatch(Singleton):
    def __init__(self):
        super(MailBatch, self).__init__()
        self.users = {}

    def add_mail(self, mail, dapp_logs):
        if mail and dapp_logs:
            if not self.users.get(mail):
                self.users[mail] = {}

            self.users[mail].update(dapp_logs)

    def send_mail(self):
        # copy users, reset the param (it allows to get more block while emails are sent)
        user_emails = self.users.copy()
        self.users = {}

        try:
            complete_url = settings.SERVER_HOST
            admin_url = reverse('api:admin')  # /api/alert/admin/

            if complete_url.endswith('/'):
                complete_url += admin_url[1:]
            else:
                complete_url += admin_url

            complete_url += '?code='

            for mail, dapp_logs in user_emails.iteritems():
                # TODO support batch mail, reuse connection
                send_email('emails/alerts.html', {'etherscan_url': settings.ETHERSCAN_URL, 'dapps': dapp_logs, 'unsubscribe_url': complete_url}, mail)
                del user_emails[mail]
        except Exception:
            for mail, dapp_logs in user_emails.iteritems():
                if not self.users.get(mail):
                    self.users[mail] = {}
                self.users[mail].update(dapp_logs)

batch = MailBatch()

def callback_per_block(filtered):
    for mail, dapp_logs in filtered.iteritems():
        batch.add_mail(mail, dapp_logs)

def callback_per_exec():
    batch.send_mail()

def filter_logs(logs, contracts):
    Alert = apps.get_app_config('events').get_model('Alert')
    # filter by contracts
    all_alerts = Alert.objects.filter(contract__in=contracts).prefetch_related('events__event_values').prefetch_related('dapp')
    filtered = {}
    for log in logs:
        # get alerts for same log contract (can be many)
        alerts = all_alerts.filter(contract=log[u'address'])

        for alert in alerts:
            # Get event names
            events = alert.events.filter(name=log[u'name'])
            if events.count():
                # Get event property, if event property, discard unmatched values
                add_event = True
                if events[0].event_values.count():
                    # check that all parameters check in value or doesn't exist
                    for event_value in events[0].event_values.iterator():
                        for param in log[u'params']:
                            if event_value.property == param[u'name']:
                                if event_value.value != param[u'value']:
                                    add_event = False

                # add log
                if add_event:
                    email = alert.dapp.user.email
                    dapp_name = alert.dapp.name
                    dapp_code = alert.dapp.authentication_code
                    if not filtered.get(email):
                        filtered[email] = {}
                    if not filtered[email].get(dapp_name):
                        # filtered[email][dapp_name] = []
                        filtered[email][dapp_name] = dict(authentication_code=dapp_code, logs=[])

                    # filtered[email][dapp_name].append(log)
                    filtered[email][dapp_name].get('logs').append(log)

    return filtered
