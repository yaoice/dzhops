# hosts.sls

{% load_yaml as install_plugin %}
config_network_interface: ${config_network_interface}
config_ha_install: ${config_ha_install}
config_lb_install: ${config_ha_install}
config_storage_install: ${config_storage_install}
config_cinder_install: true
config_neutron_install: true
config_ceilometer_install: true
config_heat_install: true
config_zabbix_install: ${config_zabbix_install}
config_elk_install: ${config_elk_install}
config_docs_install: false
{% endload %}

{% load_yaml as pkg_resource %}
yum_repo_name: Liberty
yum_repo_baseurl: http://99cloudftp:RFCQd9gO@172.16.20.14/ftp/rpms/rpms
pip_index_url: http://99cloudftp:RFCQd9gO@172.16.20.14/ftp/rpms/rpms/pypi/simple
{% endload %}

{% load_yaml as ntp %}
servers: ${ntp_servers}
ntp_server: 202.120.2.100
{% endload %}

{% load_yaml as ha %}
servers: ${controllers}
vip: ${keepalived_vip}/32
vip_hostname: openstack_vip
vip_network_interface: ${keepalived_vip_interface}
vip_set_method: keepalived
keepalived_virtual_router_id: ${keepalived_vrid}
{% endload %}

{% load_yaml as lb %}
backends: haproxy
servers: ${controllers}
{% endload %}

{% load_yaml as messagequeue %}
backends: rabbitmq
servers: ${controllers}
{% endload %}

{% load_yaml as cache %}
backends: memcached
servers: ${controllers}
{% endload %}

{% load_yaml as mariadb %}
servers: ${controllers}
arbiters:
{% endload %}

{% load_yaml as storage %}
backends: ${storage_backends}
servers: ${storage_osd_minions}
monitors: ${storage_mon_minions}
osd:
% for minion_id, devs in ceph_osd_devs_dict.items():
  ${minion_id}:
  % for dev in devs:
      ${dev}:
         journal:
  % endfor
% endfor
{% endload %}

{% load_yaml as keystone %}
servers: ${controllers}
keystone_auth_admin_user: admin
keystone_auth_admin_pass: admin
keystone_auth_region_name: ${region}
{% endload %}

{% load_yaml as glance %}
servers: ${controllers}
% if config_storage_install == 'false':
glance_image_backends: file
% elif config_storage_install == 'true':
glance_image_backends: ${storage_backends}
% endif
glance_glusterfs_voluem_bricks: /gfs/glance
glance_glusterfs_volume_name: glance
glance_glusterfs_volume_replica:
glance_rbd_store_pool: images
glance_pool_pg_num: 128
{% endload %}

{% load_yaml as nova %}
servers: ${controllers}
{% endload %}

{% load_yaml as nova_compute %}
servers: ${computes}
nova_virt_type: ${virt_type}
nova_libvirt_inject_password: True
% if config_storage_install == 'false':
nova_instances_backends: file
% elif config_storage_install == 'true':
nova_instances_backends: ${storage_backends}
% endif
nova_glusterfs_voluem_bricks: /gfs/nova
nova_glusterfs_volume_name: nova
nova_glusterfs_volume_replica:
nova_rbd_store_pool: vms
nova_pool_pg_num: 128
{% endload %}

{% load_yaml as neutron %}
servers: ${controllers}
neutron_provider_networks:
  network_flat_networks: "external"
% if neutron_mode == 'vlan':
  network_mappings: "external:br-ex,vlan:br-data"
  network_types: "vxlan,flat,vlan"
  network_vlan_ranges: "vlan:${vlan_start}:${vlan_end}"
% elif neutron_mode == 'vxlan':
  network_mappings: "external:br-ex"
  network_types: "vxlan,flat"
  network_vxlan_ranges: "${vxlan_start}:${vxlan_end}"
% endif
{% endload %}

{% load_yaml as neutron_agent %}
servers: ${neutron_ovs_minions}
{% endload %}

{% load_yaml as cinder %}
servers: ${controllers}
cinder_glusterfs_volume_name: cinder
cinder_glusterfs_voluem_bricks: /gfs/cinder
cinder_glusterfs_volume_replica:
cinder_pool_pg_num: 128
% if config_storage_install == 'true':
  % if storage_backends == 'ceph':
cinder_backends:
  ceph:
    volume_driver: "cinder.volume.drivers.rbd.RBDDriver"
    rbd_pool: volumes
    volume_backend_name: ceph
  % elif storage_backends == 'glusterfs':
cinder_backends:
  glusterfs:
    volume_driver: "cinder.volume.drivers.glusterfs.GlusterfsDriver"
    glusterfs_shares_config: "/etc/cinder/glusterfs_shares"
    glusterfs_mount_point_base: "/var/lib/cinder/mnt"
    volume_backend_name: "glusterfs"
  % endif
% endif
cinder_service_backup_program_enabled: false
cinder_service_backup_driver: cinder.backup.drivers.nfs
cinder_nfs_backup_share: "localhost:/backup"
{% endload %}

{% load_yaml as ceilometer %}
servers: ${controllers}
ceilometer_mongodb_servers: ${controllers}
ceilometer_mongodb_arbiters:
ceilometer_influxdb_servers: ${controllers}
ceilometer_compute_agents: ${computes}
{% endload %}

{% load_yaml as heat %}
servers: ${controllers}
{% endload %}

{% load_yaml as horizon %}
servers: ${controllers}
horizon_animbus_dashboard: true
{% endload %}

{% load_yaml as zabbix %}
servers: ${zabbix_servers}
agents: ${zabbix_agents}
grafana_enabled: true
zabbix_mariadb_servers: ${zabbix_servers}
{% endload %}

{% load_yaml as elk %}
elasticsearch_servers: ${elk_servers}
logstash_servers: ${elk_servers}
logstash_agents: ${elk_agents}
rabbitmq_servers: ${elk_servers}
{% endload %}

{% load_yaml as docs %}
servers: ${controllers}
docs_package_url: http://controller2/docs.tar.gz
{% endload %}
