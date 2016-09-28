# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'saltstack.views',
    # Examples:
    # url(r'^$', 'dzhops.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^execute/$', 'remoteExecute', name='execute'),
    url(r'^deploy/$', 'deployProgram', name='deploy'),
    url(r'^openstack/deploy/$', 'openstackDeployProgram', name='openstack_deploy'),
    url(r'^openstack/add/$', 'openstackAddProgram', name='openstack_add'),
    url(r'^openstack/api/deploy/$', 'openstackDeployApi', name='openstack_deploy_api'),
    url(r'^openstack/env/create/$', 'openstackEnvCreate', name='openstack_env_create'),
    url(r'^openstack/api/check_deploy_process/$', 'checkDeployProcess', name='check_deploy_process'),
    url(r'^update/$', 'updateConfig', name='update'),
    url(r'^add/$', 'addMinion', name='add_minion'),
    url(r'^index/$', 'indexMinion', name='index_minion'),
    url(r'^routine/$', 'routineMaintenance', name='routine'),
    url(r'^api/execute/$', 'remoteExecuteApi', name='execute_api'),
    url(r'^api/deploy/$', 'deployProgramApi', name='deploy_api'),
)
