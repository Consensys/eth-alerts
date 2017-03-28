from .base import *


DEBUG = env.bool("DJANGO_DEBUG", True)
SECRET_KEY = env('SECRET_KEY', default='CHANGEME!!!')

# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'
EMAIL_LOG_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#SERVER_EMAIL = '127.0.0.1'
# EMAIL_HOST = '0.0.0.0'
EMAIL_PORT = 2525
CELERY_ALWAYS_EAGER = True
ETHEREUM_NODE_SSL=""
SERVER_HOST = env('SERVER_HOST', default='http://localhost:8080')

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='giacomo.licari@gmail.com'
EMAIL_HOST_PASSWORD='hedibogodfptcyqx'
EMAIL_USE_TLS=True
