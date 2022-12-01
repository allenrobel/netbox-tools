#!/usr/bin/env python3
'''
Name: virtual_machine_create_update_one.py
Description: Create/update virtual_machine with key ``--key`` in file ``--yaml``
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

OUR_VERSION = 101

def get_parser():
    """
    return an argparse parser object
    """
    help_key = 'Key to create/update'
    help_yaml = 'YAML file containing virtual_machines information.'

    ex_prefix     = 'Example: '
    ex_key = '{} --key mycable '.format(ex_prefix)
    ex_yaml = '{} --yaml ./virtual_machines.yml'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create/update virtual_machine with key ``--key`` in file ``--yaml``')

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
if cfg.key not in info['virtual_machines']:
    print('exiting. Nothing to do.  key {} not found in yaml {}'.format(cfg.key, cfg.yaml))
    exit()

vm = VirtualMachine(nb, info['virtual_machines'][cfg.key])
vm.create_or_update()
interface_dict = get_interface_dict(info['virtual_machines'][cfg.key], info['virtual_interfaces'])
if 'ip4' not in interface_dict:
    print('virtual_machine {} interface {}, skipping ipv4 address processing since ip4 key is missing'.format(
        interface_dict['virtual_machine'],
        interface_dict['interface']
    ))
    exit(0)
i = VirtualInterface(nb, interface_dict)
i.create_or_update()
ip_addresses_dict = info['ip4_addresses']
ip_address_dict = make_ip_address_dict(ip_addresses_dict, interface_dict)
vip = VirtualIpAddress(nb, ip_address_dict)
vip.create_or_update()
