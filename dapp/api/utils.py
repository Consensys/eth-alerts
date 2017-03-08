# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from mail_templated import EmailMessage
# from django.core import mail
import hashlib
import random


def send_email(template_name, context, email_to):
    message = EmailMessage()
    message.template_name = template_name
    message.context = context
    message.from_email = settings.SERVER_EMAIL
    message.to= [email_to]
    message.send()


def get_SHA256():
    return hashlib.sha256(str(random.random())).hexdigest()
