# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .local import *


# CACHE CONFIGURATION
# ------------------------------------------------------------------------------
CACHES = {
    'default': env.cache(default='dummycache://')
}
