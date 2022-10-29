#!/usr/bin/env python3
'''
Name: location_delete_all.py
Description: Delete all locations defined in ``--yaml``

Be careful!  This will not ask for confirmation.
'''
our_version = 101
import argparse
import pynetbox
from netbox_tools.common import netbox
from netbox_tools.common import load_yaml
from netbox_tools.location import Location

help_yaml = 'Name of yaml file containing locations to delete.'

ex_prefix = ' Example: '
ex_yaml = '{} --yaml /path/to/my.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Delete all locations in YAML file')

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
for key in info['locations']:
    l = Location(nb, info['locations'][key])
    l.delete()