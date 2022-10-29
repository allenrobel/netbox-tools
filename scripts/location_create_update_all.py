#!/usr/bin/env python3
'''
Name: location_create_update_all.py
Description: Create/update locations defined in ``--yaml``.
'''
our_version = 101
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.location import Location

help_yaml = 'YAML file containing device type information.'

ex_prefix     = 'Example: '
ex_yaml = '{} --yaml ./locations.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update locations in Netbox from information in a YAML file')

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
    location = Location(nb, info['locations'][key])
    location.create_or_update()
