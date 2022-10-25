#!/usr/bin/env python3
'''
Name: device_type_create_update.py
Description: Create or update a Netbox device type using command line options
'''
our_version = 102
import argparse
import re
from lib.common import netbox, load_yaml
from lib.device_type import DeviceType

help_comments = 'Freeform comments for this device type.'
help_manufacturer = 'Who makes this device type'
help_model = 'Typically, the product/model number for this device type'
help_tags = 'A comma-separated list of tags for this device type (these must all exist in netbox already)'
ex_prefix     = 'Example: '
ex_comments = '{} --comments "36x40/100G QSFP28 Ethernet Module"'.format(ex_prefix)
ex_manufacturer = '{} --manufacturer cisco'.format(ex_prefix)
ex_model = '{} --model N9K-C9336C-FX2'.format(ex_prefix)
ex_tags = '{} --tags admin,infra'
parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update a Netbox device type (Netbox device type is roughly equivilent to model number)')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
optional   = parser.add_argument_group(title='OPTIONAL SCRIPT ARGS')

optional.add_argument('--comments',
                     dest='comments',
                     required=False,
                     default=None,
                     help=help_comments + ex_comments)

mandatory.add_argument('--manufacturer',
                     dest='manufacturer',
                     required=True,
                     help=help_manufacturer + ex_manufacturer)

mandatory.add_argument('--model',
                     dest='model',
                     required=True,
                     help=help_model + ex_model)

optional.add_argument('--tags',
                     dest='tags',
                     required=False,
                     default=None,
                     help=help_tags + ex_tags)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

nb = netbox()

info = dict()
info['manufacturer'] = cfg.manufacturer
info['model'] = cfg.model
if cfg.comments != None:
    info['comments'] = cfg.comments
if cfg.tags != None:
    info['tags'] = re.split(',', cfg.tags)

d = DeviceType(nb, info)
d.create_or_update()

