#!/usr/bin/env python3
"""
Name: device_create_update.py
Summary: Create a basic device in netbox (does not set management interface and primary ip)
See also:
    device_create_with_ip.py,
    device_create_update_all.py
    device_create_update_one.py

Example usage:

./device_create.py \
        --device dc5_leaf_1 \
        --role leaf \
        --site DC05 \
        --type N9K-C9336C-FX2
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import netbox
from netbox_tools.device import Device

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_device = "Name of the device to add."
    help_role = "Role for the device."
    help_site = "Site in which device will reside."
    help_type = "Type of device (e.g. model number)."

    ex_prefix = "Example: "
    ex_device = f"{ex_prefix} --device leaf_3"
    ex_role = f"{ex_prefix} --role leaf"
    ex_site = f"{ex_prefix} --site f1"
    ex_type = f"{ex_prefix} --type N9K-C93180YC-EX"

    parser = argparse.ArgumentParser(description="DESCRIPTION: Netbox: Add a device")

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--device", dest="device", required=True, help=f"{help_device} {ex_device}"
    )
    mandatory.add_argument(
        "--role", dest="role", required=True, help=f"{help_role} {ex_role}"
    )
    mandatory.add_argument(
        "--site", dest="site", required=True, help=f"{help_site} {ex_site}"
    )
    mandatory.add_argument(
        "--type", dest="type", required=True, help=f"{help_type} {ex_type}"
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


def get_info():
    """
    return dictionary containing all parameters expected by Device()
    """
    info = {}
    info["device"] = cfg.device
    info["type"] = cfg.type
    info["role"] = cfg.role
    info["site"] = cfg.site
    for key,value in info.items():
        if key is None:
            log(f"exiting. key {key} value {value} failed verification")
            sys.exit(1)
    return info


cfg = get_parser()
netbox_obj = netbox()
device_obj = Device(netbox_obj, get_info())
device_obj.create_or_update()
