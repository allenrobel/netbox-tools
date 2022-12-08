#!/usr/bin/env python3
"""
Name: interface_delete.py
Description: Delete interface ``--interface`` from netbox
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.interface import Interface

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_device = "Name of the device associated with --interface"
    help_interface = "Name of the interface to delete."

    ex_prefix = " Example: "
    ex_device = f"{ex_prefix} --device leaf_3"
    ex_interface = f"{ex_prefix} --interface mgmt0"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Delete interface --interface from netbox"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--device", dest="device", required=True, help=f"{help_device} {ex_device}"
    )
    mandatory.add_argument(
        "--interface",
        dest="interface",
        required=True,
        help=f"{help_interface} {ex_interface}"
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary expected by Interface().delete()
    """
    info = {}
    info["interface"] = cfg.interface
    info["device"] = cfg.device
    return info


cfg = get_parser()
netbox_obj = netbox()
interface_obj = Interface(netbox_obj, get_info())
interface_obj.delete()
