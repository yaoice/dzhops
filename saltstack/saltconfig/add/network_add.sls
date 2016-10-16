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
node_172_16_214_183: 172.16.214.183
node_172_16_214_170: 172.16.214.170
node_172_16_214_199: 172.16.214.199
node_172_16_214_198: 172.16.214.198
node_172_16_214_197: 172.16.214.197
node_172_16_214_196: 172.16.214.196
node_172_16_214_195: 172.16.214.195
node_172_16_214_194: 172.16.214.194
node_172_16_214_193: 172.16.214.193
node_172_16_214_192: 172.16.214.192
node_172_16_214_191: 172.16.214.191
node_172_16_214_190: 172.16.214.190
node_172_16_214_162: 172.16.214.162
node_172_16_214_163: 172.16.214.163
node_172_16_214_160: 172.16.214.160
node_172_16_214_161: 172.16.214.161
node_172_16_214_164: 172.16.214.164
node_172_16_214_165: 172.16.214.165
node_172_16_214_168: 172.16.214.168
node_172_16_214_169: 172.16.214.169
node_172_16_214_188: 172.16.214.188
node_172_16_214_189: 172.16.214.189
node_172_16_214_184: 172.16.214.184
node_172_16_214_185: 172.16.214.185
node_172_16_214_186: 172.16.214.186
node_172_16_214_187: 172.16.214.187
node_172_16_214_180: 172.16.214.180
node_172_16_214_181: 172.16.214.181
node_172_16_214_182: 172.16.214.182
node_172_16_214_200: 172.16.214.200
% if add_minions_hosts:
  % for id, ip in add_minions_hosts.items():
${id}: ${ip}
  % endfor
% endif
{% endload %}

{% load_yaml as storage_network_hosts %}
{% endload %}
