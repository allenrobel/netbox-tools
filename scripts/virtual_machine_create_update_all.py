#!/usr/bin/env python3
"""
Name: virtual_machine_create_update_all.py
Description: Create/update virtual_machines defined in ``--yaml``
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import netbox, load_yaml, make_ip_address_dict
from netbox_tools.virtual_machine import VirtualMachine
from netbox_tools.virtual_interface import VirtualInterface
from netbox_tools.virtual_ip_address import VirtualIpAddress

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing virtual_machines information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./virtual_machines.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update virtual_machines defined in ``--yaml``"
    )
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
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
    return interfaces_dict[interface_key]


def make_virtual_machine(netbox_object, info_dict, key):
    """
    create a virtual machine
    """
    obj = VirtualMachine(netbox_object, info_dict["virtual_machines"][key])
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


def make_virtual_machines(netbox_object, info_dict):
    """
    create all virtual machines defined in info_dict
    """
    for key in info_dict["virtual_machines"]:
        print("---")
        make_virtual_machine(netbox_object, info, key)
        interface_dict = get_interface_dict(
            info_dict["virtual_machines"][key], info_dict["virtual_interfaces"]
        )
        if "ip4" not in interface_dict:
            msg = f"virtual_machine {interface_dict['virtual_machine']}"
            msg += f" interface {interface_dict['interface']}, skipping ipv4 address processing"
            msg += " since ip4 key is missing"
            log(msg)
            continue
        make_virtual_interface(netbox_object, interface_dict)
        make_virtual_ip_address(netbox_object, interface_dict, info_dict)


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
if "virtual_machines" not in info:
    log(f"Exiting. virtual_machines are not defined in {cfg.yaml}")
    sys.exit(1)
make_virtual_machines(netbox_obj, info)
