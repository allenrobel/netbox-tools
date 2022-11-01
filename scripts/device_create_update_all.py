#!/usr/bin/env python3
'''
Name: device_create_update_all.py
Description: Create/update devices defined in ``--yaml``

This script creates/updates device, device mgmt interface, and device primary_ip 
'''
our_version = 100
import argparse
from netbox_tools.common import netbox, load_yaml, interface_id, ip_address_id
from netbox_tools.device import Device, initialize_device_primary_ip, make_device_primary_ip, map_device_primary_ip
from netbox_tools.interface import Interface
from netbox_tools.ip_address import IpAddress

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

def assign_primary_ip_to_device(info):
    ipv4_id = ip_address_id(nb, info['mgmt_ip'])
    intf_id = interface_id(nb, info['device'], info['interface'])
    if ipv4_id == None:
        print('assign_primary_ip_to_device: Exiting. Address {} not found in netbox'.format(info['mgmt_ip']))
        exit(1)
    if intf_id == None:
        print('assign_primary_ip_to_device: Exiting. Interface {} not found in netbox'.format(info['interface']))
        exit(1)
    initialize_device_primary_ip(nb, info['device'])
    map_device_primary_ip(nb, info['device'], info['interface'], info['mgmt_ip'])
    make_device_primary_ip(nb, info['device'], info['mgmt_ip'])

cfg = get_parser()
nb = netbox()
info = load_yaml(cfg.yaml)
for key in info['devices']:
    print('---')
    d = Device(nb, info['devices'][key])
    d.create_or_update()
    i = Interface(nb, info['devices'][key])
    i.create_or_update()
    ip = IpAddress(nb, info['devices'][key])
    ip.create_or_update()
    assign_primary_ip_to_device(info['devices'][key])
