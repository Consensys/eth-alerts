# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .base import *


SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = [".gnosis.pm"]

INSTALLED_APPS += ("gunicorn", )

SERVER_HOST = env('SERVER_HOST', default='https://alerts.gnosis.pm')

if DEBUG is False:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    MIDDLEWARE_CLASSES += ('whitenoise.middleware.WhiteNoiseMiddleware', )

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_HOST = env('EMAIL_HOST', default='smtp.mandrillapp.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', default='[gnosis alerts] ')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='gnosispm <noreply@gnosis.pm>')
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_BACKEND = 'email_log.backends.EmailBackend'
EMAIL_LOG_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# CELERY
# ------------------------------------------------------------------------------
CELERY_ALWAYS_EAGER = True
