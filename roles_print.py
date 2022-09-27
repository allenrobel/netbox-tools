#!/usr/bin/env python3
'''
Name: roles_print.py
Description: Display information about all device roles (e.g. role id, color, description)
'''
our_version = 101
import argparse
from lib.common import netbox
from lib.colors import rgb_to_color

parser = argparse.ArgumentParser(
         description='DESCRIPTION: retrieve and print information about all device roles')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()


def get_fmt():
    return '{:>5} {:<18} {:>12} {:<6} {:<15} {:<7} {:<30}'

def print_device_roles():
    roles = nb.dcim.device_roles.all()
    if roles == None:
        exit()
    fmt = get_fmt()
    for role in roles:
        print(fmt.format(role.id, role.name, role.device_count, role.color, rgb_to_color(role.color), role.vm_role, role.description))

def print_headers():
    fmt = get_fmt()
    print(fmt.format('id', 'role_name', 'device_count', 'rgb', 'color', 'vm_role', 'description'))
    print(fmt.format('-' * 5, '-' * 18, '-' * 12, '-' * 6, '-' * 15, '-' * 7, '-' * 30))

nb = netbox()

print_headers()
print_device_roles()