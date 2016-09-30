# network.sls

{% load_yaml as network_interface %}
manage_network_interface: eth0
storage_network_interface: eth0
data_network_interface: eth1
public_network_interface: eth2
{% endload %}

{% load_yaml as network_cidr %}
storage_network_cidr: e
data_network_cidr: 172.16.1.0/24
{% endload %}

{% load_yaml as manage_network_hosts %}
node_172_16_214_131: 172.16.214.131
node_172_16_214_114: 172.16.214.114
node_172_16_214_113: 172.16.214.113
node_172_16_214_111: 172.16.214.111
% if add_minions_hosts:
  % for id, ip in add_minions_hosts.items():
${id}: ${ip}
  % endfor
% endif
{% endload %}

{% load_yaml as storage_network_hosts %}
{% endload %}
