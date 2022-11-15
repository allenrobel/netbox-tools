#!/usr/bin/env python3
'''
Name: device_create_update_one.py
Description: Create/update device with key ``--key`` in file ``--yaml``

This script creates/updates device, device mgmt interface, and device primary_ip 
'''
our_version = 100
import argparse
from netbox_tools.common import netbox, load_yaml, interface_id, ip_address_id
from netbox_tools.device import Device, initialize_device_primary_ip, make_device_primary_ip, map_device_primary_ip
from netbox_tools.interface import Interface
from netbox_tools.ip_address import IpAddress

def get_parser():
    help_key = 'Key to create/update'
    help_yaml = 'YAML file containing devices information.'

    ex_prefix = 'Example: '
    ex_key = '{} --key mycable '.format(ex_prefix)
    ex_yaml = '{} --yaml ./devices.yml'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create/update device with key ``--key`` in file ``--yaml``')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--key',
                        dest='key',
                        required=True,
                        help=help_key + ex_key)

    mandatory.add_argument('--yaml',
                        dest='yaml',
                        required=True,
                        help=help_yaml + ex_yaml)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))
    return parser.parse_args()

def assign_primary_ip_to_device(ip, device, interface):
    ipv4_id = ip_address_id(nb, ip)
    intf_id = interface_id(nb, device, interface)
    if ipv4_id == None:
        print('assign_primary_ip_to_device: Exiting. Address {} not found in netbox'.format(ip))
        exit(1)
    if intf_id == None:
        print('assign_primary_ip_to_device: Exiting. device {} interface {} not found in netbox'.format(
            device,
            interface))
        exit(1)
    initialize_device_primary_ip(nb, device)
    map_device_primary_ip(nb, device, interface, ip)
    make_device_primary_ip(nb, device, ip)

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

if cfg.key not in info['devices']:
    print('exiting. Nothing to do.  key {} not found in yaml {}'.format(cfg.key, cfg.yaml))
    exit()
print('---')
d = Device(nb, info['devices'][cfg.key])
d.create_or_update()
interface_dict = get_interface_dict(info['devices'][cfg.key], info['interfaces'])
if 'ip4' not in interface_dict:
    print('device {} interface {}, skipping ipv4 address processing since ip4 key is missing'.format(
        interface_dict['device'],
        interface_dict['interface']
    ))
    exit(0)
i = Interface(nb, interface_dict)
i.create_or_update()
ip = IpAddress(nb, interface_dict)
ip.create_or_update()
assign_primary_ip_to_device(
    interface_dict['ip4'],
    info['devices'][cfg.key]['device'],
    interface_dict['interface'])
