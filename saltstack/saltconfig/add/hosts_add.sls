# hosts.sls

{% load_yaml as install_plugin %}
config_ha_install: true
config_lb_install: true
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
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57,${add_ntp_servers}
ntp_server: 202.120.2.100
{% endload %}

{% load_yaml as ha %}
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
vip: 172.16.214.7/32
vip_hostname: openstack_vip
vip_network_interface: eth0
vip_set_method: keepalived
keepalived_virtual_router_id: 78
{% endload %}

{% load_yaml as lb %}
backends: haproxy
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
{% endload %}

{% load_yaml as messagequeue %}
backends: rabbitmq
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
{% endload %}

{% load_yaml as cache %}
backends: memcached
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
{% endload %}

{% load_yaml as mariadb %}
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
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
  % for dev in devs:
      ${dev}:
         journal:
  % endfor
% endfor
% endif
{% endload %}

{% load_yaml as keystone %}
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
keystone_auth_admin_user: admin
keystone_auth_admin_pass: admin
keystone_auth_region_name: RegionTwo
{% endload %}

{% load_yaml as glance %}
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
glance_image_backends: file
glance_glusterfs_voluem_bricks: /gfs/glance
glance_glusterfs_volume_name: glance
glance_glusterfs_volume_replica:
glance_rbd_store_pool: images
glance_pool_pg_num: 128
{% endload %}

{% load_yaml as nova %}
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
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
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
neutron_provider_networks:
  network_flat_networks: "external"
  network_mappings: "external:br-ex,vlan:br-data"
  network_types: "vxlan,flat,vlan"
  network_vlan_ranges: "vlan::"
{% endload %}

{% load_yaml as neutron_agent %}
servers: ${neutron_ovs_minions}
{% endload %}

{% load_yaml as cinder %}
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
cinder_glusterfs_volume_name: cinder
cinder_glusterfs_voluem_bricks: /gfs/cinder
cinder_glusterfs_volume_replica:
cinder_pool_pg_num: 128
cinder_service_backup_program_enabled: false
cinder_service_backup_driver: cinder.backup.drivers.nfs
cinder_nfs_backup_share: "localhost:/backup"
{% endload %}

{% load_yaml as ceilometer %}
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
ceilometer_mongodb_servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
ceilometer_mongodb_arbiters:
ceilometer_influxdb_servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
ceilometer_compute_agents: ${computes}
{% endload %}

{% load_yaml as heat %}
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
{% endload %}

{% load_yaml as horizon %}
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
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
servers: node_172_16_214_39,node_172_16_214_40,node_172_16_214_57
docs_package_url: http://controller2/docs.tar.gz
{% endload %}
