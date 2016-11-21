# network.sls

{% load_yaml as network_interface %}
manage_network_interface: eth0
storage_network_interface: eth1
data_network_interface: eth1
public_network_interface: eth2
{% endload %}

{% load_yaml as network_cidr %}
storage_network_cidr: 172.16.115.0/24
data_network_cidr: 
{% endload %}

{% load_yaml as manage_network_hosts %}
node_172_16_214_197: 172.16.214.197
node_172_16_214_196: 172.16.214.196
node_172_16_214_195: 172.16.214.195
% if add_minions_hosts:
  % for id, ip in add_minions_hosts.items():
${id}: ${ip}
  % endfor
% endif
{% endload %}

{% load_yaml as storage_network_hosts %}
{% endload %}
