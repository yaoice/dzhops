# hosts.sls

{% load_yaml as install_plugin %}
config_network_interface: true
config_ha_install: false
config_lb_install: false
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
servers: node_248,${add_ntp_servers}
ntp_server: 202.120.2.100
{% endload %}

{% load_yaml as ha %}
servers: node_248
vip: /32
vip_hostname: openstack_vip
vip_network_interface: 
vip_set_method: keepalived
keepalived_virtual_router_id: 
{% endload %}

{% load_yaml as lb %}
backends: haproxy
servers: node_248
{% endload %}

{% load_yaml as messagequeue %}
backends: rabbitmq
servers: node_248
{% endload %}

{% load_yaml as cache %}
backends: memcached
servers: node_248
{% endload %}

{% load_yaml as mariadb %}
servers: node_248
arbiters:
{% endload %}

{% load_yaml as storage %}
backends: file
servers: ${storage_osd_minions}
monitors: 
osd:
% if add_ceph_osd_devs_dict:
% for minion_id, devs in add_ceph_osd_devs_dict.items():
  ${minion_id}:
  % for dev, journal in devs.items():
      ${dev}:
         journal: ${journal}
  % endfor
% endfor
% endif
{% endload %}

{% load_yaml as keystone %}
servers: node_248
keystone_auth_admin_user: admin
keystone_auth_admin_pass: admin
keystone_auth_region_name: RegionOne
{% endload %}

{% load_yaml as glance %}
servers: node_248
glance_image_backends: file
glance_glusterfs_voluem_bricks: /gfs/glance
glance_glusterfs_volume_name: glance
glance_glusterfs_volume_replica:
glance_rbd_store_pool: images
glance_pool_pg_num: 128
{% endload %}

{% load_yaml as nova %}
servers: node_248
{% endload %}

{% load_yaml as nova_compute %}
servers: ${computes}
nova_virt_type: kvm
nova_libvirt_inject_password: True
nova_instances_backends: ${nova_storage_backends}
nova_glusterfs_voluem_bricks: /gfs/nova
nova_glusterfs_volume_name: nova
nova_glusterfs_volume_replica:
nova_rbd_store_pool: vms
nova_pool_pg_num: 128
{% endload %}

{% load_yaml as neutron %}
servers: node_248
neutron_provider_networks:
  network_flat_networks: "external"
  network_mappings: "external:br-ex"
  network_types: "vxlan,flat"
  network_vxlan_ranges: "1:1111"
{% endload %}

{% load_yaml as neutron_agent %}
servers: ${neutron_ovs_minions}
{% endload %}

{% load_yaml as cinder %}
servers: node_248
cinder_glusterfs_volume_name: cinder
cinder_glusterfs_voluem_bricks: /gfs/cinder
cinder_glusterfs_volume_replica:
cinder_pool_pg_num: 128
cinder_service_backup_program_enabled: false
cinder_service_backup_driver: cinder.backup.drivers.nfs
cinder_nfs_backup_share: "localhost:/backup"
{% endload %}

{% load_yaml as ceilometer %}
servers: node_248
ceilometer_mongodb_servers: node_248
ceilometer_mongodb_arbiters:
ceilometer_influxdb_servers: node_248
ceilometer_compute_agents: ${computes}
{% endload %}

{% load_yaml as heat %}
servers: node_248
{% endload %}

{% load_yaml as horizon %}
servers: node_248
horizon_animbus_dashboard: true
{% endload %}

{% load_yaml as zabbix %}
servers: 
agents: ${zabbix_agents}
grafana_enabled: true
zabbix_mariadb_servers: 
{% endload %}

{% load_yaml as elk %}
elasticsearch_servers: 
logstash_servers: 
logstash_agents: ${elk_agents}
rabbitmq_servers: 
{% endload %}

{% load_yaml as docs %}
servers: node_248
docs_package_url: http://controller2/docs.tar.gz
{% endload %}
