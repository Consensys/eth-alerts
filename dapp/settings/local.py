from .base import *


DEBUG = env.bool("DJANGO_DEBUG", True)
SECRET_KEY = env('SECRET_KEY', default='CHANGEME!!!')

# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'
EMAIL_LOG_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = '127.0.0.1'

CELERY_ALWAYS_EAGER = True