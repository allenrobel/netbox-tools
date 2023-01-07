#!/usr/bin/env python3
"""
Name: vlan_group_delete.py
Description: Delete vlan_group ``--vlan_group``
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.vlan_group import VlanGroup

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_vlan_group = "Name of the VlanGroup to delete."

    ex_prefix = " Example: "
    ex_vlan_group = f"{ex_prefix} --vlan_group AdminServers"
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Delete a VlanGroup"
    )
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    mandatory.add_argument(
        "--vlan_group",
        dest="vlan_group",
        required=True,
        help=f"{help_vlan_group} {ex_vlan_group}",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )
    return parser.parse_args()


def get_info():
    """
    return dictionary containing args expected by VlanGroup
    """
    info = {}
    info["vlan_group"] = cfg.vlan_group
    return info


cfg = get_parser()
VlanGroup(netbox(), get_info()).delete()
