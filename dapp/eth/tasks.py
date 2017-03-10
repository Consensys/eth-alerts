from celery import shared_task
from bot import Bot
from celery.contrib import rdb


@shared_task
def run_bot():
    bot = Bot()
    bot.execute()