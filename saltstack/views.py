# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

from hostlist.models import DataCenter, HostList
from record.models import OperateRecord, ReturnRecord
from saltstack.models import DangerCommand, DeployModules, ConfigUpdate, CommonOperate
from saltstack.saltapi import SaltAPI
from saltstack.util import targetToMinionID, datacenterToMinionID, findJob, mysqlReturns, outFormat, manageResult, \
    moduleDetection, moduleLock, moduleUnlock, isThisRunning
#from saltstack.sshutil import auth, disable_selinux, disable_services, backup_repo_and_pip, config_repo_and_pip, \
#    create_yum_and_pip, config_salt_minion
from saltstack.sshutil import *
from dzhops import settings
from fabric.api import execute
from fabric.network import disconnect_all
# from jinja2 import Environment, FileSystemLoader
from mako.lookup import TemplateLookup

import logging, json, time, copy, os, subprocess

# Create your views here.

log = logging.getLogger('dzhops')


@login_required
def openstackDeployProgram(request):

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password']
    )
    minions_list = sapi.allMinionKeys()[0]
    # 获取ceph osd dev盘符
    osd_devices = sapi.masterToMinionContent(tgt='*',
                                             fun='ceph_osd.get_osd_dev',
                                             arg=None)
    return render(
        request,
        'openstack_deploy.html',
        {
         'minions_list': minions_list,
         'osd_devices': osd_devices
        }
    )


@csrf_exempt
@login_required
def openstackEnvCreate(request):
    template_dir = os.path.join(settings.BASE_DIR, 'saltstack/saltconfig')
    output_dir = '/srv/openstack-deploy/salt/dev/inventory/'
    network_dict = {}
    ceph_osd_devs_dict = {}
    neutron_ovs_minions = ''

    if request.method == 'POST':
        config_ha_install = request.POST.get('config_ha_install', '')
        config_storage_install = request.POST.get('config_storage_install', '')
        config_zabbix_install = request.POST.get('config_zabbix_install', '')
        config_elk_install = request.POST.get('config_elk_install', '')
        keepalived_vip = request.POST.get('keepalived_vip', '')
        keepalived_vrid = request.POST.get('keepalived_vrid', '')
        keepalived_vip_interface = \
            request.POST.get('keepalived_vip_interface', '')
        controller_minions = request.POST.get('controller_minions', '')
        compute_minions = request.POST.get('compute_minions', '')
        zabbix_server_minions = request.POST.get('zabbix_server_minions', '')
        zabbix_agent_minions = request.POST.get('zabbix_agent_minions', '')
        elk_server_minions = request.POST.get('elk_server_minions', '')
        elk_agent_minions = request.POST.get('elk_agent_minions', '')
        storage_mon_minions = request.POST.get('storage_mon_minions', '')
        storage_osd_minions = request.POST.get('storage_osd_minions', '')
        compute_minions = request.POST.get('compute_minions', '')
        storage_backends = request.POST.get('storage_backends', '')
        ceph_osd_devs_json = request.POST.get('ceph_osd_devs', '')
        ceph_osd_devs = json.loads(ceph_osd_devs_json) if ceph_osd_devs_json \
            else {}
        neutron_mode = request.POST.get('neutron_mode', '')
        vlan_start = request.POST.get('vlan_start', '')
        vlan_end = request.POST.get('vlan_end', '')
        vxlan_start = request.POST.get('vxlan_start', '')
        vxlan_end = request.POST.get('vxlan_end', '')
        manage_interface = request.POST.get('manage_interface', '')
        data_interface = request.POST.get('data_interface', '')
        storage_interface = request.POST.get('storage_interface', '')
        public_interface = request.POST.get('public_interface', '')
        storage_cidr = request.POST.get('storage_cidr', '')
        data_cidr = request.POST.get('data_cidr', '')

        for minion_id, dev in ceph_osd_devs.items():
            ceph_osd_devs_dict[minion_id] = dev.split(',')

        compute_minions_list = compute_minions.split(',')
        controller_minions_list = controller_minions.split(',')
        if config_storage_install == 'true':
            storage_mon_minions_list = storage_mon_minions.split(',')
            storage_osd_minions_list = storage_osd_minions.split(',')
            all_minions = set(controller_minions_list +
                              compute_minions_list +
                              storage_mon_minions_list +
                              storage_osd_minions_list)
        elif config_storage_install == 'false':
            all_minions = set(controller_minions_list + compute_minions_list)

        for id in all_minions:
            id_list = id.split('_')
            ip = '.'.join(id_list[1:])
            network_dict[id] = ip

        neutron_ovs_minions = ','.join(list(set(compute_minions_list +
                                       controller_minions_list)))

        salt_config_dict = {
                    'controllers': controller_minions,
                    'computes': compute_minions,
                    'zabbix_servers': zabbix_server_minions,
                    'zabbix_agents': zabbix_agent_minions,
                    'elk_servers': elk_server_minions,
                    'elk_agents': elk_agent_minions,
                    'neutron_ovs_minions': neutron_ovs_minions,
                    'config_ha_install': config_ha_install,
                    'config_storage_install': config_storage_install,
                    'config_zabbix_install': config_zabbix_install,
                    'config_elk_install': config_elk_install,
                    'storage_backends': storage_backends,
                    'storage_mon_minions': storage_mon_minions,
                    'storage_osd_minions': storage_osd_minions,
                    'ceph_osd_devs_dict': ceph_osd_devs_dict,
                    'keepalived_vip': keepalived_vip,
                    'keepalived_vrid': keepalived_vrid,
                    'keepalived_vip_interface': keepalived_vip_interface,
                    'manage_interface': manage_interface,
                    'storage_interface': storage_interface,
                    'data_interface': data_interface,
                    'public_interface': public_interface,
                    'storage_cidr': storage_cidr,
                    'data_cidr': data_cidr,
                    'minions_hosts': network_dict,
                    'neutron_mode': neutron_mode,
                    'vlan_start': vlan_start,
                    'vlan_end': vlan_end,
                    'vxlan_start': vxlan_start,
                    'vxlan_end': vxlan_end
                    }

    def genSaltConfigFile():
        env = TemplateLookup(directories=[template_dir],
                             module_directory='/tmp/mako_modules',
                             output_encoding='utf-8',
                             encoding_errors='replace')
        tpl_list = os.listdir(template_dir)
        # 渲染tpl目录下的所有模板
        for t in tpl_list:
            tpl = env.get_template(t)
            output = tpl.render(**salt_config_dict)
            with open(output_dir + t, 'w') as out:
                out.write(output)

    try:
        genSaltConfigFile()
    except:
        print "generate salt config files error"
        ret_json = json.dumps({'ret_code': 1})
        return HttpResponse(ret_json, content_type='application/json')
    ret_json = json.dumps({'ret_code': 0})
    return HttpResponse(ret_json, content_type='application/json')


@csrf_exempt
@login_required
def openstackDeployApi(request):
    cmd_dir = "/srv/openstack-deploy/salt/dev/scripts/"
    cmd_name = "all.sh"

    if isThisRunning(cmd_dir, cmd_name):
        ret_json = json.dumps({'ret_code': 2})
        return HttpResponse(ret_json, content_type='application/json')

    try:
        subprocess.Popen(('bash ' + os.path.join(cmd_dir, cmd_name)).split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    except:
        print "execute all.sh failed"
        ret_json = json.dumps({'ret_code': 1})
        return HttpResponse(ret_json, content_type='application/json')
    ret_json = json.dumps({'ret_code': 0})
    return HttpResponse(ret_json, content_type='application/json')


@login_required
def checkDeployProcess(request):
    content = ''
    with open('/var/www/html/openstack_deploy/salt_all.log') as f:
        for line in f:
            line += '</br>'
            content += line
        ret_json = json.dumps({'res': 1, 'content': content})
    return HttpResponse(ret_json, content_type='application/json')


@login_required
def deployProgram(request):
    '''
    部署程序，如部署行情程序、监控程序、账号代理程序等；
    :param request:
            目标Minions或机房、组；
            需要执行的sls文件
    :return:
            {'minion ip':{'cont':'format result','status': colour },...} ,
                hostsft:{'sum':'','rsum':'','unre':'','unrestr':'','fa':'','tr':''}
    '''
    user = request.user.username
    dcen_list = []
    sls_list = []
    data_centers = {}
    sls_mod_dict = {}

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    result_sls = DeployModules.objects.all()
    for row_data in result_sls:
        sls_mod_dict[row_data.slsfile] = row_data.module
        sls_list.append(row_data.slsfile)
    sls_list.sort()

    return render(
        request,
        'salt_deploy.html',
        {
            'dcen_list': dcen_list,
            'data_centers': data_centers,
            'sls_list': sls_list,
            'sls_mod_dict': sls_mod_dict
        }
    )


@csrf_exempt
@login_required
def addMinion(request):
    '''

    '''
    if request.method == 'POST':
        minions_list = request.POST.get('minions', '')
        master = request.POST.get('master', '')
        root_username = request.POST.get('username', '')
        root_password = request.POST.get('password', '')
        yum_url = request.POST.get('yum_url', '')
        pip_url = request.POST.get('pip_url', '')

        master_hosts = []
        minion_hosts = None
        master_hosts.append(master)
        minion_hosts = [minion for minion in minions_list.split(',')]

        kwargs = {
            'env_user': root_username,
            'env_password': root_password,
            # 'env_key_filename': '/tmp/yao.pem',
            'env_hosts': minion_hosts,
            'env_roledefs': {
                    'master': master_hosts,
                    'minion': minion_hosts,
                    }
        }

        try:
            auth(**kwargs)
            config_repo_and_pip(yum_url, pip_url, master_hosts)
            execute(disable_selinux)
            execute(disable_services)
            execute(backup_repo_and_pip)
            execute(create_yum_and_pip)
#            execute(config_salt_master)
            execute(config_salt_minion)
            disconnect_all()

        except:
            log.error("add salt minions error")
            ret_json = json.dumps({'add_res': 1})
            return HttpResponse(ret_json, content_type='application/json')

        else:
            ret_json = json.dumps({'add_res': 0})
            return HttpResponse(ret_json, content_type='application/json')


@login_required
def indexMinion(request):
    '''

    '''
    minions_list = []
    db_result = HostList.objects.all()
    for db in db_result:
        minions_list.append(db.ip)
    minions_list.sort()

    return render(
        request,
        'salt_minions.html',
        {
         'minions_list': minions_list
        }
    )


@login_required
def updateConfig(request):
    '''
    配置更新，如行情配置更新、class文件更新、ssh配置更新等；
    :param request:
    :return:
    '''
    user = request.user.username
    dcen_list = []
    data_centers = {}
    sls_list = []
    sls_mod_dict = {}

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    result_sls = ConfigUpdate.objects.all()
    for row_data in result_sls:
        sls_mod_dict[row_data.slsfile] = row_data.module
        sls_list.append(row_data.slsfile)
    sls_list.sort()

    return render(
        request,
        'salt_update.html',
        {
            'dcen_list': dcen_list,
            'data_centers': data_centers,
            'sls_list': sls_list,
            'sls_mod_dict': sls_mod_dict
        }
    )


@login_required
def routineMaintenance(request):
    '''
    日常维护操作，比如日志清理、批量重启程序等；
    :param request:
    :return:
    '''
    user = request.user.username
    dcen_list = []
    data_centers = {}
    sls_list = []
    sls_mod_dict = {}

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    result_sls = CommonOperate.objects.all()
    for row_data in result_sls:
        sls_mod_dict[row_data.slsfile] = row_data.module
        sls_list.append(row_data.slsfile)

    return render(
        request,
        'salt_routine.html',
        {
            'dcen_list': dcen_list,
            'data_centers': data_centers,
            'sls_list': sls_list,
            'sls_mod_dict': sls_mod_dict
        }
    )


@login_required
def deployProgramApi(request):
    '''
    模块部署功能，前端页面提交的数据由该函数处理，执行完毕后返回json格式数据到api；
    :param request:
    :return:
    '''
    user = request.user.username
    salt_module = 'state.sls'
    get_errors = []
    errors = []
    result_dict = {}

    if request.method == 'GET':
        check_tgt = request.GET.get('tgt', '')
        check_dc_list = request.GET.get('datacenter', '')
        check_arg = request.GET.get('sls', '')

        module_detection = moduleDetection(salt_module, user)

        if module_detection:
            get_errors.append(module_detection)
            log.debug('{0}'.format(str(module_detection)))
        if not (check_tgt or check_dc_list):
            get_errors.append(u'需要输入服务器IP或选择机房！')
            log.error('Did not enter servers ip or choose data center.')
        if not check_arg:
            get_errors.append(u'请选择将要进行的操作！')
            log.error('Not select the file of salt state.')

        if get_errors:
            for error in get_errors:
                errors.append(error.encode('utf-8'))
            result_dict['errors'] = errors
        else:
            tgt = request.GET.get('tgt', '')
            dc = request.GET.get('datacenter', '')
            arg = request.GET.get('sls', '')

            dc_clean = dc.strip(',')
            log.debug(str(dc_clean))
            dc_list = dc_clean.split(',')
            target_list = tgt.split(',')
            tgt_mixture_list = copy.deepcopy(dc_list)
            tgt_mixture_list.extend(target_list)

            if tgt:
                minion_id_from_tgt_set = targetToMinionID(tgt)
            else:
                minion_id_from_tgt_set = set([])
            if dc:
                log.debug(str(dc_list))
                minion_id_from_dc_set = datacenterToMinionID(dc_list)
            else:
                minion_id_from_dc_set = set([])
            all_minion_id_set = minion_id_from_tgt_set.union(minion_id_from_dc_set)
            # log.debug('The all target minion id set: {0}'.format(str(all_minion_id_set)))

            if all_minion_id_set:
                sapi = SaltAPI(
                    url=settings.SALT_API['url'],
                    username=settings.SALT_API['user'],
                    password=settings.SALT_API['password'])

                module_lock = moduleLock(salt_module, user)

                if '*' in tgt_mixture_list:
                    jid = sapi.asyncMasterToMinion('*', salt_module, arg)
                else:
                    tgt_list_to_str = ','.join(list(all_minion_id_set))
                    jid = sapi.asyncMasterToMinion(tgt_list_to_str, salt_module, arg)

                if dc_list:
                    operate_tgt = dc_list[0]
                elif tgt:
                    operate_tgt = target_list[0]
                else:
                    operate_tgt = 'unknown'

                op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                op_user = arg
                op_tgt = '%s...' % operate_tgt
                p1 = OperateRecord.objects.create(
                    nowtime=op_time,
                    username=user,
                    user_operate=op_user,
                    simple_tgt=op_tgt,
                    jid=jid)

                find_job = findJob(all_minion_id_set, jid)
                result = mysqlReturns(jid)
                module_unlock = moduleUnlock(salt_module, user)
                ret, hostfa, hosttr = outFormat(result)

                # log.debug(str(ret))
                recv_ips_list = ret.keys()
                send_recv_info = manageResult(all_minion_id_set, recv_ips_list)
                send_recv_info['succeed'] = hosttr
                send_recv_info['failed'] = hostfa
                saveRecord = ReturnRecord.objects.create(
                    jid=jid,
                    tgt_total=send_recv_info['send_count'],
                    tgt_ret=send_recv_info['recv_count'],
                    tgt_succ=send_recv_info['succeed'],
                    tgt_fail=send_recv_info['failed'],
                    tgt_unret=send_recv_info['unrecv_count'],
                    tgt_unret_list=send_recv_info['unrecv_strings']
                )
                result_dict['result'] = ret
                result_dict['info'] = send_recv_info
            else:
                log.info('The all target minion id set is Null.')
                set_null = u'数据库中没有找到输入的主机，请确认输入是否正确！'
                result_dict['errors'] = set_null.encode('utf-8')
    ret_json = json.dumps(result_dict)

    return HttpResponse(ret_json, content_type='application/json')


@login_required
def remoteExecute(request):
    '''
    通过SaltStack cmd.run模块，对Salt minion远程执行命令；
    :param request: None
    :return:
    '''
    user = request.user.username
    dcen_list = []
    data_centers = {}

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    return render(
        request,
        'salt_execute.html',
        {'dcen_list': dcen_list, 'data_centers': data_centers}
    )


@login_required
def remoteExecuteApi(request):
    '''
    远程执行的命令通过JQuery(ajax)提交到这里，处理后返回结果json;
    :param request:
    :return:
    '''
    user = request.user.username
    get_errors = []
    errors = []
    result_dict = {}
    danger_cmd_list = []

    danger_cmd_data = DangerCommand.objects.filter(status='True')
    if danger_cmd_data:
        for i in danger_cmd_data:
            danger_cmd_list.append(i.command)
    else:
        log.debug('The table of DangerCommand is Null.')

    if request.method == 'GET':
        check_tgt = request.GET.get('tgt', '')
        check_dc_list = request.GET.get('datacenter', '')
        check_arg = request.GET.get('arg', '')

        module_detection = moduleDetection('cmd.run', user)

        if module_detection:
            get_errors.append(module_detection)
        if not (check_tgt or check_dc_list):
            get_errors.append(u'需要指定目标主机或目标机房！')
        if not check_arg:
            get_errors.append(u'请输入将要执行的命令！')
        else:
            if danger_cmd_list:
                arg_list = check_arg.split(';')
                for i in arg_list:
                    try:
                        command = i.split()[0]
                    except IndexError, e:
                        log.debug('Command ends with a semicolon, Error info: {0}.'.format(str(e)))
                        continue
                    for j in danger_cmd_list:
                        if j in command:
                            get_errors.append(u'%s 命令危险，不允许使用！' % command)
            else:
                log.debug('Databases has not danger command')

        if get_errors:
            for error in get_errors:
                errors.append(error.encode('utf-8'))
            result_dict['errors'] = errors
        else:
            tgt = request.GET.get('tgt', '')
            dc = request.GET.get('datacenter', '')
            arg = request.GET.get('arg', '')

            dc_clean = dc.strip(',')
            log.debug(str(dc_clean))
            dc_list = dc_clean.split(',')
            target_list = tgt.split(',')
            tgt_mixture_list = copy.deepcopy(dc_list)
            tgt_mixture_list.extend(target_list)

            if tgt:
                minion_id_from_tgt_set = targetToMinionID(tgt)
            else:
                minion_id_from_tgt_set = set([])
            if dc:
                log.debug(str(dc_list))
                minion_id_from_dc_set = datacenterToMinionID(dc_list)
            else:
                minion_id_from_dc_set = set([])
            all_minion_id_set = minion_id_from_tgt_set.union(minion_id_from_dc_set)
            log.debug('The all target minion id set: {0}'.format(str(all_minion_id_set)))

            if all_minion_id_set:
                sapi = SaltAPI(
                    url=settings.SALT_API['url'],
                    username=settings.SALT_API['user'],
                    password=settings.SALT_API['password'])

                module_lock = moduleLock('cmd.run', user)

                if '*' in tgt_mixture_list:
                    jid = sapi.asyncMasterToMinion('*', 'cmd.run', arg)
                else:
                    tgt_list_to_str = ','.join(list(all_minion_id_set))
                    jid = sapi.asyncMasterToMinion(tgt_list_to_str, 'cmd.run', arg)

                if dc_list:
                    operate_tgt = dc_list[0]
                elif tgt:
                    operate_tgt = target_list[0]
                else:
                    operate_tgt = 'unknown'

                op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                op_user = arg
                op_tgt = '%s...' % operate_tgt
                p1 = OperateRecord.objects.create(
                    nowtime=op_time,
                    username=user,
                    user_operate=op_user,
                    simple_tgt=op_tgt,
                    jid=jid)

                find_job = findJob(all_minion_id_set, jid)
                result = mysqlReturns(jid)
                module_unlock = moduleUnlock('cmd.run', user)
                ret, hostfa, hosttr = outFormat(result)

                # log.debug(str(ret))
                recv_ips_list = ret.keys()
                send_recv_info = manageResult(all_minion_id_set, recv_ips_list)
                saveRecord = ReturnRecord.objects.create(
                    jid=jid,
                    tgt_total=send_recv_info['send_count'],
                    tgt_ret=send_recv_info['recv_count'],
                    tgt_unret=send_recv_info['unrecv_count'],
                    tgt_unret_list=send_recv_info['unrecv_strings']
                )
                result_dict['result'] = ret
                result_dict['info'] = send_recv_info
            else:
                log.info('The all target minion id set is Null.')
                set_null = u'数据库中没有找到输入的主机，请确认输入是否正确！'
                result_dict['errors'] = set_null.encode('utf-8')
    ret_json = json.dumps(result_dict)

    return HttpResponse(ret_json, content_type='application/json')
