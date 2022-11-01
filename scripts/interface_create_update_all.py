#!/usr/bin/env python3
'''
Name: interface_create_update_all.py
Description: Create/update all ip prefixes defined in ``--yaml``
'''
our_version = 100
import argparse

from netbox_tools.common import netbox, load_yaml
from netbox_tools.interface import Interface

help_yaml = 'YAML file in which prefix information can be found.'

ex_prefix_ = ' Example: '
ex_yaml = '{} --yaml ./info.yml'.format(ex_prefix_)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Create or update all interfaces')

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

info = load_yaml(cfg.yaml)
nb = netbox()
print('---')
for key in info['devices']:
    i = Interface(nb, info['devices'][key])
    i.create_or_update()
