# network.sls

{% load_yaml as network_interface %}
manage_network_interface: eth0
storage_network_interface: eth1
data_network_interface: eth2
public_network_interface: eth2
{% endload %}

{% load_yaml as network_cidr %}
storage_network_cidr: 10.0.0.0/24
data_network_cidr: 192.168.141.0/24
{% endload %}

{% load_yaml as manage_network_hosts %}
% if add_minions_hosts:
  % for id, ip in add_minions_hosts.items():
${id}: ${ip}
  % endfor
% endif
{% endload %}

{% load_yaml as storage_network_hosts %}
{% endload %}
