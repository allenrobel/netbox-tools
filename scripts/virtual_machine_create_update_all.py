#!/usr/bin/env python3
'''
Name: virtual_machine_create_update_all.py
Description: Create/update virtual_machines defined in ``--yaml``
'''
our_version = 100
import argparse
from netbox_tools.common import netbox, load_yaml, virtual_interface_id, ip_address_id
from netbox_tools.virtual_machine import VirtualMachine, initialize_vm_primary_ip, make_vm_primary_ip, map_vm_primary_ip
from netbox_tools.virtual_interface import VirtualInterface
from netbox_tools.virtual_ip_address import VirtualIpAddress

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
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()


def assign_primary_ip_to_vm(ip, vm, interface):
    ip4_id = ip_address_id(nb, ip)
    intf_id = virtual_interface_id(nb, vm, interface)
    if ip4_id == None:
        print('assign_primary_ip_to_vm: Exiting. Address {} not found in netbox'.format(ip))
        exit(1)
    if intf_id == None:
        print('assign_primary_ip_to_vm: Exiting. device {} interface {} not found in netbox'.format(
            vm,
            interface))
        exit(1)
    print('assign_primary_ip_to_vm: vm {} interface {} ip {} ip4_id {}'.format(vm, interface, ip, ip4_id))
    initialize_vm_primary_ip(nb, vm)
    map_vm_primary_ip(nb, vm, interface, ip)
    make_vm_primary_ip(nb, vm, ip)


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
    vip = VirtualIpAddress(nb, interface_dict)
    vip.create_or_update()
    assign_primary_ip_to_vm(
        interface_dict['ip4'],
        info['virtual_machines'][key]['vm'],
        interface_dict['interface'])
