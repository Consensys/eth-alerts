# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from mail_templated import EmailMessage


def send_email(template_name, context, email_to):
    message = EmailMessage()
    message.template_name = template_name
    message.context = context
    message.from_email = settings.SERVER_EMAIL
    message.to= [email_to]
    message.send()
