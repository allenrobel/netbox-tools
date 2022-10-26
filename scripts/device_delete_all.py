#!/usr/bin/env python3
'''
Name: device_create_all.py
Summary: Delete all devices contained in the YAML file pointed to with --yaml
Description: Delete all devices in YAML file

Be careful!  This will not ask for confirmation. 

'''
our_version = 100
import argparse
import pynetbox
from lib.common import netbox
from lib.common import load_yaml
from lib.device import Device

help_yaml = 'Name of yaml file containing devices to delete.'

ex_prefix = ' Example: '
ex_yaml = '{} --yaml /path/to/my.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Delete all devices in YAML file')

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
for key in info['devices']:
    d = Device(nb, info['devices'][key])
    d.delete()