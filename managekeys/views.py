# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView

from hostlist.models import HostList, DataCenter, Dzhuser
from saltstack.saltapi import SaltAPI
from managekeys.utils import clearUpMinionKyes

from dzhops import settings

import logging
import json
# Create your views here.

log = logging.getLogger('opsmaster')


@login_required
def manageMinionKeys(request):
    '''
    进入页面，首次展示已经接受的所有Minion ID，从这里获取并返回；
    :param request:
    :return:
    '''
    user = request.user.username
    serv_list = []
    ip_list = []
    serv_dict = {}
    dc_dict = {}
    engi_dict ={}

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password']
    )
    minions, minions_pre, minions_rej = sapi.allMinionKeys()
    # log.debug(str(minions))

    dcs = DataCenter.objects.all()
    for dc in dcs:
        dc_dict[dc.dcen] = dc.dccn
    egs = Dzhuser.objects.all()
    for eg in egs:
        engi_dict[eg.username] = eg.engineer

    for id in minions:
        ip = sapi.masterToMinionContent(tgt=id,
                                        fun='ip.get_ipv4',
                                        arg=None).get(id) or '127.0.0.1'
        if ip == '127.0.0.1':
            log.error("ManageKeys: {0} does not get local ipv4".format(id))
        ip_list.append(ip)
        serv_dict[ip] = id
    ip_list.sort()
    for i in ip_list:
        ipid_dict = {}
        id = serv_dict.get(i)
        ipid_dict[i] = id
        serv_list.append(ipid_dict)
        del ipid_dict

    return render(
        request,
        'manage_keys.html',
        {
            'dc_dict': dc_dict,
            'engi_dict': engi_dict,
            'serv_list': serv_list,
        }
    )


class ManageKeysView(ListView):
    template_name = 'manage_keys.html'
    context_object_name = 'node_list'
    
    def get_servers(self):
        serv_list = []
        ip_list = []
        serv_dict = {}

        sapi = SaltAPI(
            url=settings.SALT_API['url'],
            username=settings.SALT_API['user'],
            password=settings.SALT_API['password']
        )
        minions, minions_pre, minions_rej = sapi.allMinionKeys()
        # log.debug(str(minions))

        for id in minions:
            ip = sapi.masterToMinionContent(tgt=id,
                                            fun='ip.get_ipv4',
                                            arg=None).get(id) or id + ' does not get correct ip'
            if 'does not get correct ip' in ip:
                log.error("ManageKeys: {0} does not get local ipv4".format(id))
            ip_list.append(ip)
            serv_dict[ip] = id
        ip_list.sort()

        for i in ip_list:
            ipid_dict = {}
            id = serv_dict.get(i)
            ipid_dict[i] = id
            serv_list.append(ipid_dict)
            del ipid_dict
        return serv_list

    def get_dcs(self):
        dc_dict = {}
        dcs = DataCenter.objects.all()
        for dc in dcs:
            dc_dict[dc.dcen] = dc.dccn
        return dc_dict
    
    def get_egs(self):
        engi_dict = {}
        egs = Dzhuser.objects.all()
        for eg in egs:
            engi_dict[eg.username] = eg.engineer
        return engi_dict
    
    def get_queryset(self):
        node_list = self.get_servers()
        return node_list

    def get_context_data(self, **kwargs):
        kwargs['dc_dict'] = self.get_dcs()
        kwargs['engi_dict'] = self.get_egs()
        return super(ManageKeysView, self).get_context_data(**kwargs)


@login_required
def getNodeTopology(request):
    '''
    进入页面，首次展示已经接受的所有Minion ID，从这里获取并返回；
    :param request:
    :return:
    '''
    serv_dict = {}
    role_list = []

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password']
    )
    minions, minions_pre, minions_rej = sapi.allMinionKeys()

    role_dict = sapi.masterToMinionContent(tgt='*',
                                           fun='grains.get',
                                           arg='role')

    for id in minions:
        ip = sapi.masterToMinionContent(tgt=id,
                                        fun='ip.get_ipv4',
                                        arg=None).get(id) or '127.0.0.1'
        if ip == '127.0.0.1':
            log.error("ManageKeys: {0} does not get local ipv4".format(id))

        roles = role_dict.get(id)
        if roles:
            roles_list = roles if isinstance(roles, list) else roles.split(',')
            role_list += roles_list
            serv_dict[id] = {'ip': ip,
                             'role': ', '.join(roles_list)}

    return render(
        request,
        'node_topology.html',
        {
#            'serv_dict': sorted(serv_dict.items(), lambda x, y: cmp(x[0], y[0]))
            'serv_list': sorted(serv_dict.items(), key=lambda d: d[0]),
            'serv_dict': json.dumps(serv_dict),
            'role_list': json.dumps(list(set(role_list))),
        }
    )


@login_required
def manageMinionKeysAPI(request):
    '''
    前端选择不同状态、机房、维护人员下的Minion id相关信息，通过ajax后台请求并刷新页面；
    :param request:
    :return: [
                {'192.168.220.201': 'CNET_HQ_SH_BETA_192_168_220_201'},
                {'192.168.220.202': 'CNET_HQ_SH_BETA_192_168_220_202'},
                ...
             ]
    '''
    user = request.user.username
    ip_list = []
    serv_list = []
    serv_dict = {}

    if request.method == 'GET':
        column = request.GET.get('col', '')
        dcen = request.GET.get('dcen', '')
        engi = request.GET.get('engi', '')

        sapi = SaltAPI(
            url=settings.SALT_API['url'],
            username=settings.SALT_API['user'],
            password=settings.SALT_API['password']
        )
        minions, minions_pre, minions_rej = sapi.allMinionKeys()

        if column == 'acp':
            result = clearUpMinionKyes(minions, dcen, engi)
        elif column == 'pre':
            result = clearUpMinionKyes(minions_pre, dcen, engi)
        elif column == 'rej':
            result = clearUpMinionKyes(minions_rej, dcen, engi)
        else:
            log.error("Unexpected execution here.")

        for id in result:
            id_list = id.split('_')
            ip = '.'.join(id_list[4:])
            ip_list.append(ip)
            serv_dict[ip] = id
        ip_list.sort()
        for i in ip_list:
            ipid_dict = {}
            id = serv_dict.get(i)
            ipid_dict[i] = id
            serv_list.append(ipid_dict)
            del ipid_dict
    else:
        log.error("Request the wrong way, need to GET method.")

    keys_json = json.dumps(serv_list)

    return HttpResponse(keys_json, content_type="application/json")


@login_required
def actionMinionKeys(request, action):
    '''
    管理minion keys，根据url捕获操作，如接受、拒绝、删除；
    :param request: 'zhaogb-201,zhaogb-202,...,'（注意：有逗号结尾的字符串）
    :param action: 通过url捕获的accept/reject/delect;
    :return:
    '''
    action = action
    minion_id = request.GET.get('minion_id')
    minion_id_strings = minion_id.strip(',')

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    ret = sapi.actionKyes(minion_id_strings, action)

    result_json = json.dumps(ret)

    return HttpResponse(result_json, content_type='application/json')


@login_required
def minionKeysAccept(request):
    '''
    展示Master已经接受的所有Minion keys；
    :param request:
    :return:
    '''
    user = request.user.username
    dccn_list = []
    dc_hosts = {}

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password']
    )

    minions, minions_pre, minions_rej = sapi.allMinionKeys()
    minions_set = set(minions)

    dcs = DataCenter.objects.all()
    for dc in dcs:
        minion_info_dict = {}
        hosts = HostList.objects.filter(dccn=dc.dccn)
        dccn_list.append(dc.dccn)
        for host in hosts:
            minion_id = host.minionid
            if minion_id in minions_set:
                minion_info_dict[minion_id] = host.ip
        dc_hosts[dc.dccn] = minion_info_dict

    dccn_list.sort()

    return render(
        request,
        'manage_keys_accept.html',
        {
            'all_dc_list': dccn_list,
            'all_dc_hosts': dc_hosts
        }
    )


@login_required
def minionKeysUnaccept(request):
    '''
    展示待接受的minion keys;
    :param request:
    :return:
    '''
    user = request.user.username
    dccn_list = []
    dc_hosts = {}

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    minions, minions_pre, minions_rej = sapi.allMinionKeys()
    minions_pre_set = set(minions_pre)

    dcs = DataCenter.objects.all()
    for dc in dcs:
        minion_info_dict = {}
        hosts = HostList.objects.filter(dccn=dc.dccn)
        dccn_list.append(dc.dccn)
        for host in hosts:
            minion_id = host.minionid
            if minion_id in minions_pre_set:
                minion_info_dict[minion_id] = host.ip
        dc_hosts[dc.dccn] = minion_info_dict
    dccn_list.sort()

    return render(
        request,
        'manage_keys_unaccept.html',
        {
            'all_dc_list': dccn_list,
            'all_minions_pre': dc_hosts
        }
    )


@login_required
def minionKeysReject(request):
    '''
    展示已经被拒绝的Minino keys；
    :param request:
    :return:
    '''
    user = request.user.username
    dccn_list = []
    dc_hosts = {}
    dc_hosts_keys = {}

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    minions, minions_pre, minions_rej = sapi.allMinionKeys()
    minions_rej_set = set(minions_rej)

    dcs = DataCenter.objects.all()
    for dc in dcs:
        minion_info_dict = {}
        hosts = HostList.objects.filter(dccn=dc.dccn)
        dccn_list.append(dc.dccn)
        for host in hosts:
            minion_id = host.minionid
            if minion_id in minions_rej_set:
                minion_info_dict[minion_id] = host.ip
        dc_hosts[dc.dccn] = minion_info_dict
    dccn_list.sort()

    return render(
        request,
        'manage_keys_reject.html',
        {
            'all_dc_list': dccn_list,
            'all_minions_rej': dc_hosts
        }
    )


@login_required
def deleteMinionKeys(request):
    '''
    删除已经接受的minion keys；
    :param request:
    :return:
    '''

    minion_id = request.GET.get('minion_id')
    minion_id_strings = minion_id.strip(',')

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    ret = sapi.deleteKeys(minion_id_strings)

    return HttpResponseRedirect(reverse('keys_show'))


@login_required
def acceptMinionKeys(request):
    '''
    Master将待接受的minion keys接受；
    :param request:
    :return:
    '''
    minion_id = request.GET.get('minion_id')
    minion_id_strings = ','.join(minion_id_list)
    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    ret = sapi.acceptKeys(minion_id_strings)

    return HttpResponseRedirect(reverse('keys_unaccept'))


@login_required
def deleteRejectKeys(request):
    '''
    Master删除已经拒绝的minion keys;
    :param request:
    :return:
    '''
    minion_id_list = request.GET.getlist('rejectkeys')
    minion_id_strings = ','.join(minion_id_list)

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    ret = sapi.deleteKeys(minion_id_strings)

    return HttpResponseRedirect(reverse('keys_reject'))
