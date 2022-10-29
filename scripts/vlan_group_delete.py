#!/usr/bin/env python3
'''
Name: vlan_group_delete.py
Description: Delete vlan_group ``--vlan_group``
'''
our_version = 102
import argparse

from netbox_tools.common import netbox
from netbox_tools.vlan_group import VlanGroup

help_vlan_group = 'Name of the VlanGroup to delete.'

ex_prefix = ' Example: '
ex_vlan_group = '{} --vlan_group AdminServers'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a VlanGroup')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--vlan_group',
                     dest='vlan_group',
                     required=True,
                     help=help_vlan_group + ex_vlan_group)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['vlan_group'] = cfg.vlan_group
    return info

nb = netbox()
d = VlanGroup(nb, get_info())
d.delete()
