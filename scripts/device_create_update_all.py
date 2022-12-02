#!/usr/bin/env python3
"""
Name: device_create_update_all.py
Description: Create/update devices defined in ``--yaml``

create/update device, device mgmt interface, and device primary_ip
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

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing devices information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./devices.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update devices defined in ``--yaml``"
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


def get_interface_dict(device_dict, interfaces_dict):
    """
    Use the value of 'interface' key in device_dict to lookup and return the associated interface
    in the interfaces_dict.

    Exit with error if device_dict does not contain an 'interface' key.
    Exit with error if value of the device_dict 'interface' key is not found in interfaces_dict.
    """
    if "interface" not in device_dict:
        log(
            f"exiting. interface key not found in device_dict {device_dict}"
        )
        sys.exit(1)
    interface_key = device_dict["interface"]
    if interface_key not in interfaces_dict:
        log(
            "exiting.",
            f"Interface {interface_key} not found in {cfg.yaml}",
            f"interfaces {interfaces_dict.keys()}.",
        )
        sys.exit(1)
    return interfaces_dict[interface_key]


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)

for key in info["devices"]:
    print("---")
    device_obj = Device(netbox_obj, info["devices"][key])
    device_obj.create_or_update()
    interface_dict = get_interface_dict(info["devices"][key], info["interfaces"])
    if "ip4" not in interface_dict:
        device_name = interface_dict["device"]
        interface_name = interface_dict["interface"]
        log(
            f"device {device_name} interface {interface_name}",
            "skipping ipv4 address processing since ip4 key is missing",
        )
        continue
    interface_obj = Interface(netbox_obj, interface_dict)
    interface_obj.create_or_update()
    ip_addresses_dict = info["ip4_addresses"]
    ip_address_dict = make_ip_address_dict(ip_addresses_dict, interface_dict)
    ip_address_obj = IpAddress(netbox_obj, ip_address_dict)
    ip_address_obj.create_or_update()
