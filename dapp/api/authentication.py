# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from events.models import User


class AuthCodeAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_code = request.META.get('auth-code')
        if auth_code:
            try:
                user = User.objects.get(authentication_code=auth_code)
                return user, None
            except User.DoesNotExist:
                raise AuthenticationFailed('Forbidden')
        else:
            raise AuthenticationFailed('Forbidden')