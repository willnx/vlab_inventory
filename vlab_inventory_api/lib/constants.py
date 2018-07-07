# -*- coding: UTF-8 -*-
"""
All the things can override via Environment variables are keep in this one file.

.. note::
    Any and all values that *are* passwords must contain the string 'AUTH' in
    the name of the constant. This is how we avoid logging passwords.
"""
from os import environ
from collections import namedtuple, OrderedDict

try:
    with open('/etc/vlab/auth_server/private.key') as the_file:
        secret = the_file.read()
    with open('/etc/vlab/auth_server/public.key') as the_file:
        pub_key = the_file.read()
except OSError:
    # assume testing env
    secret = 'testing'
    pub_key = 'testing'

DEFINED = OrderedDict([
            ('VLAB_INVENTORY_LOG_LEVEL', environ.get('VLAB_INVENTORY_LOG_LEVEL', 'INFO')),
            ('INF_VCENTER_SERVER', environ.get('INF_VCENTER_SERVER', 'localhost')),
            ('INF_VCENTER_PORT', int(environ.get('INFO_VCENTER_PORT', 443))),
            ('INF_VCENTER_USER', environ.get('INF_VCENTER_SERVER', 'tester')),
            ('INF_VCENTER_PASSWORD', environ.get('INF_VCENTER_PASSWORD', 'a')),
            ('INF_VCENTER_TOP_LVL_DIR', environ.get('INF_VCENTER_TOP_LVL_DIR', 'vlab')),
            ('INF_VCENTER_VERIFY_CERT', environ.get('INF_VCENTER_VERIFY_CERT', False)),
            ('VLAB_MESSAGE_BROKER', environ.get('VLAB_MESSAGE_BROKER', 'inventory-broker')),
            ('VLAB_URL', environ.get('VLAB_URL', 'https://localhost')),
          ])

Constants = namedtuple('Constants', list(DEFINED.keys()))

# The '*' expands the list, just liked passing a function *args
const = Constants(*list(DEFINED.values()))
