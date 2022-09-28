#!/usr/bin/env python3
'''
Name: role_delete.py
Description: Delete role --role from netbox
'''
our_version = 100
import argparse

from lib.common import netbox
from lib.role import Role

help_role = 'Name of the role to delete.'

ex_prefix = ' Example: '
ex_role = '{} --role myrole'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a role')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--role',
                     dest='role',
                     required=True,
                     help=help_role + ex_role)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.role
    return info

nb = netbox()
d = Role(nb, get_info())
d.delete()
