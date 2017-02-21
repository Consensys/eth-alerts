from .base import *


DEBUG = env.bool("DJANGO_DEBUG", True)
SECRET_KEY = env('SECRET_KEY', default='CHANGEME!!!')