#!/usr/bin/env python3
'''
Name: role_print.py
Description: Print information about a device role
'''
our_version = 100
import argparse
import pynetbox
from lib.credentials import NetboxCredentials
from lib.colors import rgb_to_color

help_role = 'Role for the device.'

ex_prefix     = 'Example: '
ex_role = '{} --role leaf'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Print information about a device role')

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

fmt = '{:>5} {:<15} {:>12} {:<6} {:<15} {:<7} {:<30}'

def error():
    roles = list()
    items = nb.dcim.device_roles.all()
    for item in items:
        roles.append(item.name)
    print('Role {} does not exist in netbox.  Valid roles: {}'.format(cfg.role, ', '.join(roles)))
    exit(1)
def get_device_role():
    role = nb.dcim.device_roles.get(name=cfg.role)
    if role == None:
        error()
    return role

def print_headers():
    print(fmt.format('id', 'role_name', 'device_count', 'rgb', 'color', 'vm_role', 'description'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 12, '-' * 6, '-' * 15, '-' * 7, '-' * 30))

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)

role = get_device_role()
print_headers()
print(fmt.format(role.id, role.name, role.device_count, role.color, rgb_to_color(role.color), role.vm_role, role.description))
