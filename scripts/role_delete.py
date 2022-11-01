#!/usr/bin/env python3
'''
Name: role_delete.py
Description: Delete role ``--role``
'''
our_version = 102
import argparse

from netbox_tools.common import netbox
from netbox_tools.role import Role

def get_parser():
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

    return parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.role
    return info

cfg = get_parser()
nb = netbox()
d = Role(nb, get_info())
d.delete()
