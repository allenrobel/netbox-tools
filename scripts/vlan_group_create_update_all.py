#!/usr/bin/env python3
'''
Name: vlan_group_create_update_all.py
Description: Create/update vlan_groups defined in ``--yaml``
'''
our_version = 102
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.vlan_group import VlanGroup

def get_parser():
    help_yaml = 'YAML file containing VlanGroup information.'

    ex_prefix     = 'Example: '
    ex_yaml = '{} --yaml ./vlan_groups.yml'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create or update VlanGroups in Netbox from information in a YAML file')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--yaml',
                        dest='yaml',
                        required=True,
                        help=help_yaml + ex_yaml)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

cfg = get_parser()
nb = netbox()
info = load_yaml(cfg.yaml)
for key in info['vlan_groups']:
    vlan_group = VlanGroup(nb, info['vlan_groups'][key])
    vlan_group.create_or_update()
