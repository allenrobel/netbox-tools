#!/usr/bin/env python3
'''
Name: roles_create_update.py
Description: Create or update the Netbox device roles described in YAML file --yaml

If the roles already exist in netbox, they will be updated with the current information in the YAML file.
If the roles do not already exist in netbox, they will be created

Example YAML file is given below.

# device role color choices (use RGB values as the color: field value)
# 009688 : Teal
# 4caf50 : Green
# 2196f3 : Blue
# 9c27b0 : Purple
# ffeb3b : Yellow
# ff9800 : Orange
# f44336 : Red
# c0c0c0 : Light Gray
# 9e9e9e : Medium Gray
# 607d8b : Dark Gray

# device_roles mandatory fields:
#   - name
#   - color 
---
device_roles:
  leaf:
    name: leaf
    color: 009688
    description: leaf switches
  spine:
    name: spine
    color: 9c27b0
    description: spine switches
  border_gateway:
    name: border_gateway
    color: 4caf50
    description: spine switches


'''
our_version = 101
import argparse
# import re
# from string import punctuation
# import yaml
from lib.common import netbox, load_yaml
# from lib.colors import color, color_to_rgb
from lib.role import Role

help_yaml = 'YAML file containing device_roles'

ex_prefix     = 'Example: '
ex_yaml = '{} --yaml ./info.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update roles described in YAML file')

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
for key in info['device_roles']:
    r = Role(nb, info['device_roles'][key])
    r.create_or_update()
