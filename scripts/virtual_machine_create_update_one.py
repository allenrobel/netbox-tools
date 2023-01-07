#!/usr/bin/env python3
"""
Name: virtual_machine_create_update_one.py
Description: Create/update virtual_machine with key ``--key`` in file ``--yaml``
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import netbox, load_yaml, make_ip_address_dict
from netbox_tools.virtual_machine import VirtualMachine
from netbox_tools.virtual_interface import VirtualInterface
from netbox_tools.virtual_ip_address import VirtualIpAddress

OUR_VERSION = 102


def get_parser():
    """
    return an argparse parser object
    """
    help_key = "Key to create/update"
    help_yaml = "YAML file containing virtual_machines information."

    ex_prefix = "Example: "
    ex_key = f"{ex_prefix} --key virtual_machine_1 "
    ex_yaml = f"{ex_prefix} --yaml ./virtual_machines.yml"

    description = "DESCRIPTION: Create/update virtual_machine with key ``--key``"
    description += " in file ``--yaml``"
    parser = argparse.ArgumentParser(description=description)
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    mandatory.add_argument(
        "--key", dest="key", required=True, help=f"{help_key} {ex_key}"
    )
    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=f"{help_yaml} {ex_yaml}"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )
    return parser.parse_args()


def log(*args):
    """
    simple logger
    """
    print(f"{stack()[1].function}(v{OUR_VERSION}): {' '.join(args)}")


def make_virtual_machine(netbox_object, vm_info):
    """
    create a virtual machine
    """
    obj = VirtualMachine(netbox_object, vm_info)
    obj.create_or_update()


def make_virtual_interface(netbox_object, interface_dict):
    """
    create a virtual interface
    """
    obj = VirtualInterface(netbox_object, interface_dict)
    obj.create_or_update()


def make_virtual_ip_address(netbox_object, interface_dict, info_dict):
    """
    create an ip address for a virtual machine
    """
    ip_address_dict = make_ip_address_dict(info_dict["ip4_addresses"], interface_dict)
    obj = VirtualIpAddress(netbox_object, ip_address_dict)
    obj.create_or_update()


def get_interface_dict(vm_dict, interfaces_dict):
    """
    Return a dictionary containing parameters that VirtualInterface expects
    """
    if "interface" not in vm_dict:
        log(f"Exiting. interface key not found in vm_dict {vm_dict}")
        sys.exit(1)
    interface_key = vm_dict["interface"]
    if interface_key not in interfaces_dict:
        msg = f"Exiting. Interface {interface_key} not found in {cfg.yaml}"
        msg += f" interfaces {interfaces_dict.keys()}."
        log(msg)
        sys.exit(1)
    interface_dict = interfaces_dict[interface_key]
    if "ip4" not in interface_dict:
        msg = f"virtual_machine {interface_dict['virtual_machine']}"
        msg += f"interface {interface_dict['interface']},"
        msg += " skipping ipv4 address processing since ip4 key is missing"
        log(msg)
        sys.exit(0)
    return interface_dict


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
if "virtual_machines" not in info:
    log(f"Exiting. virtual_machines are not defined in {cfg.yaml}")
    sys.exit(1)
vms = info["virtual_machines"]
vints = info["virtual_interfaces"]
if cfg.key not in vms:
    log(f"Exiting. Nothing to do. key {cfg.key} not found in yaml {cfg.yaml}")
    sys.exit(0)

make_virtual_machine(netbox_obj, vms[cfg.key])
make_virtual_interface(netbox_obj, get_interface_dict(vms[cfg.key], vints))
make_virtual_ip_address(netbox_obj, get_interface_dict(vms[cfg.key], vints), info)
