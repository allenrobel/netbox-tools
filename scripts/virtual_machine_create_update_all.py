#!/usr/bin/env python3
'''
Name: virtual_machine_create_update_all.py
Description: Create/update virtual_machines defined in ``--yaml``
'''
import argparse
from netbox_tools.common import (
    netbox,
    load_yaml,
    make_ip_address_dict
)
from netbox_tools.virtual_machine import VirtualMachine
from netbox_tools.virtual_interface import VirtualInterface
from netbox_tools.virtual_ip_address import VirtualIpAddress

OUR_VERSION = 102

def get_parser():
    help_yaml = 'YAML file containing virtual_machines information.'

    ex_prefix     = 'Example: '
    ex_yaml = '{} --yaml ./virtual_machines.yml'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create/update virtual_machines defined in ``--yaml``')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--yaml',
                        dest='yaml',
                        required=True,
                        help=help_yaml + ex_yaml)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(OUR_VERSION))

    return parser.parse_args()


def get_interface_dict(vm_dict, interfaces_dict):
    if 'interface' not in vm_dict:
        print('get_interface: exiting. interface key not found in device_dict {}'.format(vm_dict))
        exit(1)
    interface_key = vm_dict['interface']
    if interface_key not in interfaces_dict:
        print('get_interface: exiting. Interface {} not found in {} interfaces {}.'.format(interface_key, cfg.yaml, interfaces_dict.keys()))
        exit(1)
    return interfaces_dict[interface_key]


cfg = get_parser()
nb = netbox()
info = load_yaml(cfg.yaml)
if 'virtual_machines' not in info:
    print('exiting. virtual_machines are not defined in {}'.format(cfg.yaml))
    exit(1)

for key in info['virtual_machines']:
    print('---')
    vm = VirtualMachine(nb, info['virtual_machines'][key])
    vm.create_or_update()
    interface_dict = get_interface_dict(info['virtual_machines'][key], info['virtual_interfaces'])
    if 'ip4' not in interface_dict:
        print('virtual_machine {} interface {}, skipping ipv4 address processing since ip4 key is missing'.format(
            interface_dict['virtual_machine'],
            interface_dict['interface']
        ))
        continue
    i = VirtualInterface(nb, interface_dict)
    i.create_or_update()
    ip_addresses_dict = info['ip4_addresses']
    ip_address_dict = make_ip_address_dict(ip_addresses_dict, interface_dict)
    vip = VirtualIpAddress(nb, ip_address_dict)
    vip.create_or_update()
