# -*- coding: utf-8 -*-
'''
Ceph-Osd module
'''
from __future__ import absolute_import
import pyudev
import re

def get_osd_dev(*args):
    '''
    Get ceph osd disk device

    CLI Example:

    .. code-block:: bash

        salt '*' ceph_osd.get_osd_dev
    '''

    context = pyudev.Context()
    pattern = re.compile('^/dev/[v|s]d[a-z]')

    osd_devices = []
    for device in context.list_devices(DEVTYPE='disk'):
        major = device['MAJOR']
        if major == '8' or re.search(pattern, device.device_node):
             osd_devices.append(device.device_node)
    return osd_devices
