#!/usr/bin/env python3
"""
Name: device_create_update_one.py
Description: Create/update device with key ``--key`` in file ``--yaml``

This script creates/updates device, device mgmt interface, and device primary_ip
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import (
    netbox,
    load_yaml,
    make_ip_address_dict,
)
from netbox_tools.device import Device
from netbox_tools.interface import Interface
from netbox_tools.ip_address import IpAddress

OUR_VERSION = 101


def get_parser():
    """
    return an argparse parser object
    """
    help_key = "Key to create/update"
    help_yaml = "YAML file containing devices information."

    ex_prefix = "Example: "
    ex_key = f"{ex_prefix} --key mycable "
    ex_yaml = f"{ex_prefix} --yaml ./devices.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update device with key ``--key`` in file ``--yaml``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    mandatory.add_argument(
        "--key", dest="key", required=True, help=f"{help_key} {ex_key}"
    )
    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=f"{help_yaml} {ex_yaml}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s v{OUR_VERSION}"
    )
    return parser.parse_args()


def log(*args):
    """
    simple logger
    """
    print(f"{stack()[1].function}(v{OUR_VERSION}): {' '.join(args)}")


def get_interface_dict(device_dict, interfaces_dict):
    """
    Return a dictionary for a specific interface

    Parameters:
    device_dict - The device dictionary containing the interface.
    interfaces_dict - The complete interfaces dictionary from --yaml
    """
    if "interface" not in device_dict:
        log(
            "get_interface: exiting.",
            f"interface key not found in device_dict {device_dict}",
        )
        sys.exit(1)
    interface_key = device_dict["interface"]
    if interface_key not in interfaces_dict:
        log(
            "get_interface: exiting.",
            f"Interface {interface_key} not found in {cfg.yaml}",
            f"interfaces {interfaces_dict.keys()}.",
        )
        sys.exit(1)
    return interfaces_dict[interface_key]


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)

if cfg.key not in info["devices"]:
    log(f"exiting. Nothing to do.  key {cfg.key} not found in yaml {cfg.yaml}")
    sys.exit()
print("---")
device_obj = Device(netbox_obj, info["devices"][cfg.key])
device_obj.create_or_update()
interface_dict = get_interface_dict(info["devices"][cfg.key], info["interfaces"])
if "ip4" not in interface_dict:
    log(
        f"device {interface_dict['device']} interface {interface_dict['interface']}.",
        "missing ip4 key. skipping ipv4 address processing",
    )
    sys.exit(0)
interface_obj = Interface(netbox_obj, interface_dict)
interface_obj.create_or_update()
ip_addresses_dict = info["ip4_addresses"]
ip_address_dict = make_ip_address_dict(ip_addresses_dict, interface_dict)
ip_address_obj = IpAddress(netbox_obj, ip_address_dict)
ip_address_obj.create_or_update()
