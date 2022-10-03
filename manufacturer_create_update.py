#!/usr/bin/env python3
'''
Name: manufacturer_create_update.py
Description: Create or update a Netbox device type.
'''
our_version = 100
import argparse
from lib.common import netbox, load_yaml
from lib.manufacturer import Manufacturer

help_manufacturer = 'Who makes this product'
ex_prefix     = 'Example: '
ex_manufacturer = '{} --manufacturer cisco'.format(ex_prefix)
parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update a Netbox manufacturer')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
optional   = parser.add_argument_group(title='OPTIONAL SCRIPT ARGS')

mandatory.add_argument('--manufacturer',
                     dest='manufacturer',
                     required=True,
                     help=help_manufacturer + ex_manufacturer)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

nb = netbox()

info = dict()
info['name'] = cfg.manufacturer

m = Manufacturer(nb, info)
m.create_or_update()

