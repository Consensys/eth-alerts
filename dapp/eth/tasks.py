from celery import shared_task
from bot import Bot
from mail_batch import MailBatch


@shared_task
def run_bot():
    bot = Bot()
    if not bot.is_running():
        bot.start()


@shared_task
def send_mails():
    batch = MailBatch()
    batch.send_mail()