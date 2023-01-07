#!/usr/bin/env python3
"""
Name: vlan_delete.py
Description: Delete vlan ``--vlan``
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.vlan import Vlan

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_vlan_name = "Name of the vlan to delete."

    ex_prefix = " Example: "
    ex_vlan_name = f"{ex_prefix} --vlan_name "

    parser = argparse.ArgumentParser(description="DESCRIPTION: Netbox: Delete a vlan")
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    mandatory.add_argument(
        "--vlan_name",
        dest="vlan_name",
        required=True,
        help=f"{help_vlan_name} {ex_vlan_name}",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )
    return parser.parse_args()


def get_info():
    """
    return dictionary containing parameters expected by Vlan
    """
    info = {}
    info["vlan_name"] = cfg.vlan_name
    return info


cfg = get_parser()
netbox_obj = netbox()
vlan_obj = Vlan(netbox_obj, get_info())
vlan_obj.delete()
