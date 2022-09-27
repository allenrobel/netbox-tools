#!/usr/bin/env python3
'''
Name: role_print.py
Description: Print information about a device role
'''
our_version = 101
import argparse
import json
from lib.common import netbox
from lib.colors import rgb_to_color

help_detail = 'Optional. If present, print detailed info about role.'
help_role = 'Role for the device.'

ex_prefix     = 'Example: '
ex_detail = '{} --detail'.format(ex_prefix)
ex_role = '{} --role leaf'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Print information about a device role')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

default.add_argument('--detail',
                     dest='detail',
                     required=False,
                     default=False,
                     action='store_true',
                     help=help_detail + ex_detail)
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

def print_detail():
    pretty = json.dumps(dict(role), indent=4, sort_keys=True)
    print(pretty)

def print_headers():
    print(fmt.format('id', 'role_name', 'device_count', 'rgb', 'color', 'vm_role', 'description'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 12, '-' * 6, '-' * 15, '-' * 7, '-' * 30))

nb = netbox()

role = get_device_role()
if cfg.detail:
    print_detail()
    exit()

print_headers()
print(fmt.format(role.id, role.name, role.device_count, role.color, rgb_to_color(role.color), role.vm_role, role.description))
