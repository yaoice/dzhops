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
node_172_16_214_158: 172.16.214.158
% if add_minions_hosts:
  % for id, ip in add_minions_hosts.items():
${id}: ${ip}
  % endfor
% endif
{% endload %}

{% load_yaml as storage_network_hosts %}
{% endload %}
