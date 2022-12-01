#!/usr/bin/env python3
'''
Name: device_create_update_all.py
Description: Create/update devices defined in ``--yaml``

create/update device, device mgmt interface, and device primary_ip 
'''
import argparse
from netbox_tools.common import (
    netbox,
    load_yaml,
    interface_id,
    ip_address_id,
    make_ip_address_dict
)
from netbox_tools.device import (
    Device,
    initialize_device_primary_ip,
    make_device_primary_ip,
    map_device_primary_ip
)
from netbox_tools.interface import Interface
from netbox_tools.ip_address import IpAddress

our_version = 102

def get_parser():
    help_yaml = 'YAML file containing devices information.'

    ex_prefix     = 'Example: '
    ex_yaml = '{} --yaml ./devices.yml'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create/update devices defined in ``--yaml``')

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

def get_interface_dict(device_dict, interfaces_dict):
    if 'interface' not in device_dict:
        print('get_interface: exiting. interface key not found in device_dict {}'.format(device_dict))
        exit(1)
    interface_key = device_dict['interface']
    if interface_key not in interfaces_dict:
        print('get_interface: exiting. Interface {} not found in {} interfaces {}.'.format(interface_key, cfg.yaml, interfaces_dict.keys()))
        exit(1)
    return interfaces_dict[interface_key]

cfg = get_parser()
nb = netbox()
info = load_yaml(cfg.yaml)

for key in info['devices']:
    print('---')
    d = Device(nb, info['devices'][key])
    d.create_or_update()
    interface_dict = get_interface_dict(info['devices'][key], info['interfaces'])
    if 'ip4' not in interface_dict:
        print('device {} interface {}, skipping ipv4 address processing since ip4 key is missing'.format(
            interface_dict['device'],
            interface_dict['interface']
        ))
        continue
    i = Interface(nb, interface_dict)
    i.create_or_update()
    ip_addresses_dict = info['ip4_addresses']
    ip_address_dict = make_ip_address_dict(ip_addresses_dict, interface_dict)
    ip = IpAddress(nb, ip_address_dict)
    ip.create_or_update()
