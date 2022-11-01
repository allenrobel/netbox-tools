#!/usr/bin/env python3
'''
Name: ip_prefix_create_update_all.py
Description: Create/update all ip prefixes defined in ``--yaml``
'''
our_version = 103
import argparse

from netbox_tools.common import netbox, load_yaml
from netbox_tools.ip_prefix import IpPrefix

def get_parser():
    help_yaml = 'YAML file in which prefix information can be found.'

    ex_prefix_ = ' Example: '
    ex_yaml = '{} --yaml ./info.yml'.format(ex_prefix_)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Netbox: Create or update all ip prefixes')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--yaml',
                        dest='yaml',
                        required=True,
                        help=help_yaml + ex_yaml)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

cfg = get_parser()
info = load_yaml(cfg.yaml)
nb = netbox()
print('---')
for key in info['prefixes']:
    p = IpPrefix(nb, info['prefixes'][key])
    p.create_or_update()
