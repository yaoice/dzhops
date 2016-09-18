# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('hostlist.views',
    # Examples:
    # url(r'^$', 'oms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^asset/$', 'assetList', name='asset_list'),
    url(r'^asset/api/$', 'assetListAPI', name='asset_api'),
)
