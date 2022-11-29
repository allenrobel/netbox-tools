#!/usr/bin/env python3
'''
Name: ip_address_create_update_all.py
Description: Create/update all ip addresses defined in ``--yaml``
'''
our_version = 100
import argparse

from netbox_tools.common import netbox, load_yaml
from netbox_tools.ip_address import IpAddress

def get_parser():
    help_yaml = 'YAML file in which ip_address information can be found.'

    ex_prefix_ = ' Example: '
    ex_yaml = '{} --yaml ./info.yml'.format(ex_prefix_)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create/update all ip addresses defined in ``--yaml``')

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

def make_ip_address_dict(info_dict, interface_dict):
    """
    Return a dictionary with the keys expected by the IpAddress class.
    """
    if 'ip4' not in interface_dict:
        return None
    if 'ip4_addresses' not in info_dict:
        return interface_dict
    ip4 = interface_dict['ip4']
    if ip4 not in info_dict['ip4_addresses']:
        return interface_dict
    ip_address_dict = interface_dict
    if 'status' in info_dict['ip4_addresses'][ip4]:
        ip_address_dict['status'] = info_dict['ip4_addresses'][ip4]['status']
    if 'role' in info_dict['ip4_addresses'][ip4]:
        ip_address_dict['role'] = info_dict['ip4_addresses'][ip4]['role']
    return ip_address_dict

cfg = get_parser()
info = load_yaml(cfg.yaml)
nb = netbox()
for key in info['interfaces']:
    ip_address_dict = make_ip_address_dict(info, info['interfaces'][key])
    if ip_address_dict is None:
        continue
    print('---')
    ip = IpAddress(nb, ip_address_dict)
    ip.create_or_update()
