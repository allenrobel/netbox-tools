#!/usr/bin/env python3
'''
Name: vlan_create_update_all.py
Description: Create or update vlans in Netbox from information in a YAML file.
'''
our_version = 100
import argparse
from lib.common import netbox, load_yaml
from lib.vlan import Vlan

help_yaml = 'YAML file containing Vlan information.'

ex_prefix     = 'Example: '
ex_yaml = '{} --yaml ./vlans.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update vlans in Netbox from information in a YAML file')

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
if 'vlans' not in info:
    print('exiting. no vlans to process in {}'.format(cfg.yaml))
    exit(1)
for key in info['vlans']:
    vlan = Vlan(nb, info['vlans'][key])
    vlan.create_or_update()