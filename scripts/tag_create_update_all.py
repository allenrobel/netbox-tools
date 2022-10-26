#!/usr/bin/env python3
'''
Name: tag_create_update_all.py
Description: Create/update tags defined in ``--yaml``
'''
our_version = 100
import argparse
from lib.common import netbox, load_yaml
from lib.tag import Tag

help_yaml = 'YAML file containing device type information.'

ex_prefix     = 'Example: '
ex_yaml = '{} --yaml ./tags.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update tags in Netbox from information in a YAML file')

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
for key in info['tags']:
    tag = Tag(nb, info['tags'][key])
    tag.create_or_update()
