# network.sls

{% load_yaml as network_interface %}
manage_network_interface: eth0
storage_network_interface: eth0
data_network_interface: eth0
public_network_interface: eth0
{% endload %}

{% load_yaml as network_cidr %}
storage_network_cidr: 
data_network_cidr: 
{% endload %}

{% load_yaml as manage_network_hosts %}
node_172_16_214_229: 172.16.214.229
node_172_16_214_228: 172.16.214.228
node_172_16_214_227: 172.16.214.227
node_172_16_214_230: 172.16.214.230
node_172_16_214_226: 172.16.214.226
% if add_minions_hosts:
  % for id, ip in add_minions_hosts.items():
${id}: ${ip}
  % endfor
% endif
{% endload %}

{% load_yaml as storage_network_hosts %}
{% endload %}
