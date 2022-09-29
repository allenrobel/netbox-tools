#!/usr/bin/env python3
'''
Name: device_create_all.py
Summary: Delete all devices contained in the YAML file pointed to with --yaml
Description: Delete device --device from netbox
'''
our_version = 100
import argparse
import pynetbox

from lib.common import netbox
from lib.device import Device

help_device = 'Name of the device to delete.'

ex_prefix = ' Example: '
ex_device = '{} --device leaf_3'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a device')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--device',
                     dest='device',
                     required=True,
                     help=help_device + ex_device)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['device'] = cfg.device
    return info

nb = netbox()
d = Device(nb, get_info())
d.delete()
