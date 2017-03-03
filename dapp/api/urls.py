# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from dapp.api import views

urlpatterns = [
    url(r'^alert/$', views.AlertView.as_view(), name='alert'),
    url(r'^alert/$', views.AlertView.as_view(), name='alert-delete'),
    url(r'^alert/confirm/(?P<confirmation_key>[a-zA-Z0-9]+)/$', views.AlertConfirmView.as_view(), name='alert-confirm'),
    url(r'^alert/delete/(?P<delete_key>[a-zA-Z0-9]+)/$', views.AlertDeleteView.as_view(), name='alert-delete-confirm'),
    url(r'^alert/signup/$', views.SignupView.as_view(), name='signup')

]