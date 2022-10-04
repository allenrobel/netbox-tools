#!/usr/bin/env python3
'''
Name: role_create_update.py
Description: Create or update a Netbox role.
Example Usage:

./role_create_update.py --role leaf --color green_dark --description "leaf switches" --tags ecmp_16,500w

NOTE: --color is currently limited to the set of colors defined in colors.py
'''
our_version = 100
import argparse
from lib.common import netbox, load_yaml
from lib.role import Role
import re

help_color = 'Color to associate with --role'
help_description = 'Free-form description for --role'
help_role = 'role name'
help_tags = 'Comma-separated list of tags (no spaces) to apply to this role. All tags must already exist in Netbox.'

ex_prefix     = 'Example: '
ex_color = '{} --color green'.format(ex_prefix)
ex_description = '{} --description "this is a role description"'.format(ex_prefix)
ex_role = '{} --role C004'.format(ex_prefix)
ex_tags = '{} --tags admin,infra'.format(ex_prefix)
parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update a Netbox role')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
optional   = parser.add_argument_group(title='OPTIONAL SCRIPT ARGS')

mandatory.add_argument('--color',
                     dest='color',
                     required=True,
                     help=help_color + ex_color)
optional.add_argument('--description',
                     dest='description',
                     required=False,
                     default=None,
                     help=help_description + ex_description)
mandatory.add_argument('--role',
                     dest='role',
                     required=True,
                     help=help_role + ex_role)
mandatory.add_argument('--tags',
                     dest='tags',
                     required=False,
                     default=None,
                     help=help_tags + ex_tags)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.role
    info['color'] = cfg.color
    if cfg.description != None:
        info['description'] = cfg.description
    if cfg.tags != None:
        info['tags'] = re.split(',', cfg.tags)
    return info

nb = netbox()
info = get_info()
role = Role(nb, info)
role.create_or_update()

