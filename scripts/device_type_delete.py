#!/usr/bin/env python3
"""
Name: device_type_delete.py
Description: Delete device_type ``--model`` from netbox
"""
import argparse

from netbox_tools.common import netbox
from netbox_tools.device_type import DeviceType

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_model = "Model number for the device type."
    ex_prefix = " Example: "
    ex_model = f"{ex_prefix} --model N9K-C9336C-FX2"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Delete a device_type"
    )
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--model", dest="model", required=True, help=f"{help_model} {ex_model}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary expected by DeviceType() delete method
    """
    info = {}
    info["model"] = cfg.model
    return info


cfg = get_parser()
netbox_obj = netbox()
d = DeviceType(netbox_obj, get_info())
d.delete()
