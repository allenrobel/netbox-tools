#!/usr/bin/env python3
'''
Name: device_type_create_update_all.py
Description: Create/update device types from information in a YAML file
'''
our_version = 101
import argparse
from lib.common import netbox, load_yaml
from lib.device_type import DeviceType

help_yaml = 'YAML file containing device type information.'

ex_prefix     = 'Example: '
ex_yaml = '{} --yaml ./device_types.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update Netbox device types (Netbox device type is roughly equivilent to NX-OS model number)')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--yaml',
                     dest='yaml',
                     required=True,
                     help=help_yaml + ex_yaml)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

nb = netbox()
info = load_yaml(cfg.yaml)
for key in info['device_types']:
    device_type = DeviceType(nb, info['device_types'][key])
    device_type.create_or_update()
