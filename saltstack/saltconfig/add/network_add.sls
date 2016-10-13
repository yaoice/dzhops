# network.sls

{% load_yaml as network_interface %}
manage_network_interface: eth0
storage_network_interface: eth0
data_network_interface: eth1
public_network_interface: 
{% endload %}

{% load_yaml as network_cidr %}
storage_network_cidr: 
data_network_cidr: 
{% endload %}

{% load_yaml as manage_network_hosts %}
node_172_16_214_162: 172.16.214.162
node_172_16_214_163: 172.16.214.163
node_172_16_214_161: 172.16.214.161
node_172_16_214_164: 172.16.214.164
node_172_16_214_165: 172.16.214.165
node_172_16_214_168: 172.16.214.168
% if add_minions_hosts:
  % for id, ip in add_minions_hosts.items():
${id}: ${ip}
  % endfor
% endif
{% endload %}

{% load_yaml as storage_network_hosts %}
{% endload %}
