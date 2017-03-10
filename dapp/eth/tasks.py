from celery import shared_task
from bot import Bot


@shared_task
def run_bot():
    bot = Bot()
    bot.execute()