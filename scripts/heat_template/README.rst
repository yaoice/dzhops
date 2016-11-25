=================================
create instances use excel apply
=================================

Install python env
-------------------

   .. code-block:: language

       [centos@zjn-dev ~]$ yum install python-pip
       [centos@zjn-dev ~]$ pip install xlrd mako shade

Configure OpenStack auth and Application info
-----------------------------------------------

   Edit cloud.yaml configuration file

   .. code-block:: language

       [centos@zjn-dev ~]$ vim cloud.yaml

Create apply stack
--------------------

   Ensure in heat_template directory before implementing python heat_template.py

   .. code-block:: language

       [centos@zjn-dev ~]$ sudo python heat_template.py

Show now stacks
-----------------------

   .. code-block:: language

       [centos@zjn-dev ~]$ openstack stack list

Delete expired stack
-----------------------

   .. code-block:: language

       [centos@zjn-dev ~]$ openstack stack delete stack_name

