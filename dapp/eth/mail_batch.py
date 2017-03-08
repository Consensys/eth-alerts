from utils import Singleton
from api.utils import send_email


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
            for mail, dapp_logs in user_emails.iteritems():
                send_email('emails/alerts.html', {'dapps': dapp_logs}, mail)
                del user_emails[mail]
        except Exception:
            for mail, dapp_logs in user_emails.iteritems():
                if not self.users.get(mail):
                    self.users[mail] = {}
                self.users[mail].update(dapp_logs)