# -*- coding: utf-8 -*-
'''
Ceph-Osd module
'''
from __future__ import absolute_import
import psutil
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
    root_partitions = [partition.device for partition in
                       psutil.disk_partitions() if partition.mountpoint == '/']

    pattern = re.compile('^/dev/[v|s|h]d[a-z]')

    osd_devices = []
    for device in context.list_devices(DEVTYPE='disk'):
        major = device['MAJOR']
        if (major == '8' or re.search(pattern, device.device_node)) and \
           not re.search(re.compile(device.device_node), root_partitions[0]):
                osd_devices.append(device.device_node)
    return osd_devices
