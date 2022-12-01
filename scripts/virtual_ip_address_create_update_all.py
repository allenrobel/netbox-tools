#!/usr/bin/env python3
'''
Name: virtual_ip_address_create_update_all.py
Description: Create/update all virtual_ip_addresses (those belonging to virtual machines) defined in ``--yaml``
'''
our_version = 100
import argparse

from netbox_tools.common import netbox, load_yaml, make_ip_address_dict
from netbox_tools.virtual_ip_address import VirtualIpAddress

def get_parser():
    help_yaml = 'YAML file in which ip_address information can be found.'

    ex_prefix_ = ' Example: '
    ex_yaml = '{} --yaml ./info.yml'.format(ex_prefix_)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Netbox: Create or update all ip addresses defined in ``--yaml``')

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
for key in info['virtual_interfaces']:
    if 'ip4' not in info['virtual_interfaces'][key]:
        continue
    ip_address_dict = make_ip_address_dict(info['ip4_addresses'], info['virtual_interfaces'][key])
    vip = VirtualIpAddress(nb, ip_address_dict)
    vip.create_or_update()
