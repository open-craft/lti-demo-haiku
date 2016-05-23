# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lti/', include('django_lti_tool_provider.urls')),
    url(r'^', include('haiku.urls', namespace='haiku')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
