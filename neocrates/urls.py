"""neocrates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from index.views import DumpIndex

from player.urls import urlpatterns as player_urls
from cas.urls import urlpatterns as cas_urls
import cas

import django.contrib.auth.views



urlpatterns = [
    url(r'dump/AudioFiles',DumpIndex.as_view(), name='dump'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cas', include(cas_urls)),

    url(r'^accounts/login',django.contrib.auth.views.login,{'template_name':'crates/login.html'}),
    url(r'^accounts/logout',django.contrib.auth.views.logout, {'next_page': '/'}),
] + player_urls # player should exist at root
