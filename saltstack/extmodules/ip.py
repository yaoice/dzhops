# -*- coding: utf-8 -*-
'''
get ipv4 module
'''
from __future__ import absolute_import
from oslo_utils import netutils


def get_ipv4(*args):
    '''
    Get ipv4

    CLI Example:

    .. code-block:: bash

        salt '*' ip.get_ipv4
    '''

    return netutils.get_my_ipv4()
