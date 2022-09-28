#!/usr/bin/env python3
'''
Name: device_type_delete.py
Description: Delete device_type from netbox
'''
our_version = 100
import argparse

from lib.common import netbox
from lib.device_type import DeviceType

help_model = 'Model number for the device type.'

ex_prefix = ' Example: '
ex_model = '{} --model N9K-C9336C-FX2'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a device_type')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')

mandatory.add_argument('--model',
                     dest='model',
                     required=True,
                     help=help_model + ex_model)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['model'] = cfg.model
    return info

nb = netbox()
d = DeviceType(nb, get_info())
d.delete()
