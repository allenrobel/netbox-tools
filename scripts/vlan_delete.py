#!/usr/bin/env python3
'''
Name: vlan_delete.py
Description: Delete vlan ``--vlan``
'''
our_version = 100
import argparse

from lib.common import netbox
from lib.vlan import Vlan

help_vlan_name = 'Name of the vlan to delete.'

ex_prefix = ' Example: '
ex_vlan_name = '{} --vlan_name '.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a vlan')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--vlan_name',
                     dest='vlan_name',
                     required=True,
                     help=help_vlan_name + ex_vlan_name)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['vlan_name'] = cfg.vlan_name
    return info

nb = netbox()
d = Vlan(nb, get_info())
d.delete()
