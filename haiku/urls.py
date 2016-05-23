# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from . import views

app_name = 'haiku'
urlpatterns = [
    url(r'^$', views.ShowOrCreateHaikuView.as_view(), name='home'),
    url(r'^add', views.CreateHaikuView.as_view(), name='add'),
    url(r'^list', views.ListHaikuView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)', views.ShowHaikuView.as_view(), name='view'),
    url(r'^edit/(?P<pk>\d+)', views.UpdateHaikuView.as_view(), name='edit'),
]
