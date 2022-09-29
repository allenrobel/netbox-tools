#!/usr/bin/env python3
'''
Name: manufacturer_create_update_all.py
Description: Create or update manufacturers in Netbox from information in a YAML file.
'''
our_version = 100
import argparse
from lib.common import netbox, load_yaml
from lib.manufacturer import Manufacturer

help_yaml = 'YAML file containing device type information.'

ex_prefix     = 'Example: '
ex_yaml = '{} --yaml ./manufacturers.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update manufacturers in Netbox from information in a YAML file')

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
for key in info['manufacturers']:
    manufacturer = Manufacturer(nb, info['manufacturers'][key])
    manufacturer.create_or_update()
