# -*- coding: utf-8 -*-


import re
import os
import yaml
from fabric.api import hosts
from fabric.api import task
from fabric.api import env
from fabric.api import sudo
from fabric.api import put
from fabric.api import parallel
from fabric.api import roles
from fabric.api import execute
from fabric.api import settings
from fabric.colors import red, green
from fabric.network import disconnect_all
from hostlist.models import HostList

from oslo_utils import netutils
from dzhops import settings as dj_settings

disable_srvs = ['firewalld']


def auth(**env_args):
    def get(key, default=None):
        return env_args.get('env_' + key, default)

    env.hosts = get('hosts', 'localhost')
    env.user = get('user', 'root')
    env.password = get('password')
    env.key_filename = get('key_filename')
    env.roledefs = get('roledefs')
    env.abort_on_prompts = True


@task
def disable_selinux():
    selinux_status = sudo('getenforce')
    if selinux_status == 'Enforcing':
        sudo('setenforce 0')
        cmd = r"sed -i -r 's/(^SELINUX=).*/\1disabled/g' /etc/selinux/config"
        sudo(cmd)
        print(green("Disable selinux now"))
    else:
        print(green("Maintain selinux status: %s" % selinux_status))


@task
def disable_services():
    with settings(warn_only=True):
        for srv in disable_srvs:
            print srv
            srv_is_exist = sudo('systemctl list-units | grep {}'.format(srv))
            if srv_is_exist.return_code == 0:
                srv_status = sudo('systemctl is-active {}'.format(srv))
                if srv_status.return_code == 0:
                    sudo('systemctl stop {}'.format(srv))
                    sudo('systemctl disable {}'.format(srv))
                    print(green("Disable {} service".format(srv)))
                else:
                    print(green("{} service alreay in inactive status.".format(srv)))
            else:
                print(red("{} service does not exist.".format(srv)))


@task
def backup_repo_and_pip():
    sudo('mkdir -p /root/.pip')
    sudo('rm -rf /etc/yum.repos.d/*')


def config_repo_and_pip(yum_url, pip_url, master_hosts):
    yum_repo_baseurl = yum_url
    pip_index_url = pip_url

    global yum_repo_content
    global pip_conf_content
    global master
    master = master_hosts[0]
    yum_repo_content = '''
[Liberty]
gpgcheck=0
humanname=liberty
baseurl={}
name=liberty
EOF
    '''.format(yum_repo_baseurl)

    pip_conf_content = '''
[global]
trusted-host=*
index-url={}
EOF
    '''.format(pip_index_url)


@task
def create_yum_and_pip():
    sudo('cat > /etc/yum.repos.d/animbus.repo << EOF {}'.format(yum_repo_content))
    sudo('yum clean all')
    sudo('cat > /root/.pip/pip.conf << EOF {}'.format(pip_conf_content))
    sudo('yum install -y python-pip')


@task
@roles('master')
def config_salt_master():
    sudo('yum install -y salt-master vim')

    salt_master_conf = '''
# interface: interface_ip
auto_accept: True
worker_threads: 10
file_recv: True
file_recv_max_size: 1000
cachedir: /srv/openstack-deploy/salt/cache
#max_event_size: 2097152
file_roots:
   base:
     - /srv/openstack-deploy/salt/
   dev:
     - /srv/openstack-deploy/salt/dev
jinja_trim_blocks: True
jinja_lstrip_blocks: True
return: mysql
master_job_cache: mysql
ext_job_cache: mysql
mysql.host: '172.16.214.110'
mysql.user: 'dzhops'
mysql.pass: 'dzhinternet'
mysql.db: 'dzhops'
mysql.port: 3306
EOF
    '''
    sudo('cat > /etc/salt/master << EOF {}'.format(salt_master_conf))
    sudo('systemctl start salt-master')
    sudo('systemctl enable salt-master')


@task
@parallel(pool_size=30)
@roles('minion')
def config_salt_minion():
    sudo('yum install -y salt-minion python2-oslo-utils python-psutil')
    sudo('rm -f /etc/salt/minion_id')

    salt_minion_conf = '''
master: {0}
mysql.host: {1}
mysql.user: {2}
mysql.pass: {3}
mysql.db: {4}
mysql.port: {5}
EOF
    '''.format(master,
               dj_settings.DATABASES['default']['HOST'],
               dj_settings.DATABASES['default']['USER'],
               dj_settings.DATABASES['default']['PASSWORD'],
               dj_settings.DATABASES['default']['NAME'],
               dj_settings.DATABASES['default']['PORT'],
               )
    ceph_osd_module_path = os.path.join(dj_settings.BASE_DIR,
                                        'saltstack/extmodules/ceph_osd.py')
    get_ipv4_module_path = os.path.join(dj_settings.BASE_DIR,
                                        'saltstack/extmodules/ip.py')

    put(ceph_osd_module_path,
        "/usr/lib/python2.7/site-packages/salt/modules/ceph_osd.py",
        mode=0644, use_sudo=True)
    put(get_ipv4_module_path,
        "/usr/lib/python2.7/site-packages/salt/modules/ip.py",
        mode=0644, use_sudo=True)

    sudo('cat > /etc/salt/minion << EOF {}'.format(salt_minion_conf))
    minion_ip = sudo("python -c 'from oslo_utils import netutils; print netutils.get_my_ipv4()'")
    host = HostList.objects.get(ip=minion_ip)
    minion_id = host.hostname or ('node_' + minion_ip.replace('.', '_'))
    sudo('hostnamectl set-hostname {}'.format(minion_id))
    sudo('systemctl restart salt-minion')
    sudo('systemctl enable salt-minion')


@task
def main():
        pass
#     auth(**kwargs)
#     config_repo_and_pip(yum_url, pip_url)
#     execute(disable_selinux)
#     execute(disable_services)
#     execute(backup_repo_and_pip)
#     execute(create_yum_and_pip)
#     execute(config_salt_master)
#     execute(config_salt_minion)
#     disconnect_all()


if __name__ == '__main__':
    main()
