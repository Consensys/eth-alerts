# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^alert/$', views.AlertView.as_view(), name='alert'),
    url(r'^alert/$', views.AlertView.as_view(), name='alert-delete'),
    url(r'^alert/signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^alert/manage/$', views.AdminView.as_view(), name='admin')
]
