#!/usr/bin/env python3
'''
Name: device_create.py
Summary: Create a basic device in netbox (does not set management interface and primary ip)
See also: device_create_with_ip.py, device_create_all.py

Example usage:

./device_create.py \
        --device dc5_leaf_1 \
        --role leaf \
        --site DC05 \
        --type N9K-C9336C-FX2
'''
our_version = 101
import pynetbox
import argparse

from lib.common import netbox
from lib.device import Device

help_device = 'Name of the device to add.'
help_role = 'Role for the device.'
help_site = 'Site in which device will reside.'
help_type = 'Type of device (e.g. model number).'

ex_prefix = 'Example: '
ex_device = '{} --device leaf_3'.format(ex_prefix)
ex_role = '{} --role leaf'.format(ex_prefix)
ex_site = '{} --site f1'.format(ex_prefix)
ex_type = '{} --type N9K-C93180YC-EX'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Add a device')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--device',
                     dest='device',
                     required=True,
                     help=help_device + ex_device)
mandatory.add_argument('--role',
                     dest='role',
                     required=True,
                     help=help_role + ex_role)
mandatory.add_argument('--site',
                     dest='site',
                     required=True,
                     help=help_site + ex_site)
mandatory.add_argument('--type',
                     dest='type',
                     required=True,
                     help=help_type + ex_type)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.device
    info['type'] = cfg.type
    info['role'] = cfg.role
    info['site'] = cfg.site
    for k in info:
        if info[k] == None:
            print('get_info: exiting. key "{}" value "{}" failed verification'.format(k, info[k]))
            exit(1)
    return info

nb = netbox()
d = Device(nb, get_info())
d.create_or_update()
