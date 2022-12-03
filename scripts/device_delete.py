#!/usr/bin/env python3
"""
Name: device_create_all.py
Summary: Delete all devices contained in the YAML file pointed to with --yaml
Description: Delete device --device from netbox
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.device import Device

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_device = "Name of the device to delete."

    ex_prefix = " Example: "
    ex_device = f"{ex_prefix} --device leaf_3"

    parser = argparse.ArgumentParser(description="DESCRIPTION: Netbox: Delete a device")

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--device", dest="device", required=True, help=f"{help_device} {ex_device}"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )
    return parser.parse_args()


def get_info():
    """
    return delete operation parameters expected by Device()
    """
    info = {}
    info["device"] = cfg.device
    return info


cfg = get_parser()
netbox_obj = netbox()
device_obj = Device(netbox_obj, get_info())
device_obj.delete()
