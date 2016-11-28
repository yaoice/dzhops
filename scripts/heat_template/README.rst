=================================
create instances use excel apply
=================================

Install python env
-------------------

   .. code-block:: language

       [centos@zjn-dev ~]$ yum install python-pip
       [centos@zjn-dev ~]$ pip install xlrd mako shade futures python-openstackclient

Configure OpenStack auth and Application info
-----------------------------------------------

   Edit cloud.yaml configuration file

   .. code-block:: language

        clouds:
            myfavoriteopenstack:
                auth:
                    # OpenStack auth info
                    auth_url: http://172.16.201.250:35357
                    username: yaoxiabing
                    password: 'password'
                    # notice: stack create in project, please use project_id,
                    # not use project name.
                    project_name: "yaoxiabing"
                    domain_name: default
                region_name: RegionOne

        #apply exccel name, ensure excel file in heat_template directory.
        excel_name: 'test.xlsx' 

Create apply stack
--------------------

   Ensure in heat_template directory before implementing python heat_template.py

   .. code-block:: language

       [centos@zjn-dev ~]$ python heat_template.py

	This script will create some stacks from application.

Show now stacks
-----------------------

   .. code-block:: language

        [centos@zjn-dev ~]$ source openstackrc(user auth info for OpenStack)
        [centos@zjn-dev ~]$ openstack stack list

Delete expired stack
-----------------------

   .. code-block:: language

       [centos@zjn-dev ~]$ openstack stack delete stack_name

