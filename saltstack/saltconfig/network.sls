# network.sls

{% load_yaml as network_interface %}
manage_network_interface: ${manage_interface}
storage_network_interface: ${storage_interface}
data_network_interface: ${data_interface}
public_network_interface: ${public_interface}
{% endload %}

{% load_yaml as network_cidr %}
storage_network_cidr: ${storage_cidr}
data_network_cidr: ${data_cidr}
{% endload %}

{% load_yaml as manage_network_hosts %}
% for id, ip in minions_hosts.items():
${id}: ${ip}
% endfor
{% endload %}

{% load_yaml as storage_network_hosts %}
{% endload %}
