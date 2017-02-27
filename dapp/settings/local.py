from .base import *


DEBUG = env.bool("DJANGO_DEBUG", True)
SECRET_KEY = env('SECRET_KEY', default='CHANGEME!!!')

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_LOG_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = '127.0.0.1'