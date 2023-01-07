#!/usr/bin/env python3
"""
Name: vlan_group_create_update.py
Description: Create/update a Netbox vlan_group using command line options
Example Usage:

./vlan_group_create_update.py \
    --vlan_group AdminServers \
    --min_vid 1 \
    --max_vid 15 \
    --description "Admin Server Vlans" \
    --tags server,admin

"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.vlan_group import VlanGroup

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_description = "Optional. Free-form description for this VlanGroup. "
    help_max_vid = "Optional. Maximum vlan id for this VlanGroup. Default: 1 "
    help_min_vid = "Optional. Minimum vlan id for this VlanGroup. Default: 4094 "
    help_tags = (
        "Optional. Comma-separated list of tags (no spaces) to apply to this VlanGroup."
    )
    help_tags += " All tags must already exist in Netbox."
    help_vlan_group = "Name of this VlanGroup"

    ex_prefix = "Example: "
    ex_description = f'{ex_prefix} --description "this is a vlan_group description"'
    ex_max_vid = f"{ex_prefix} --max_vid 10"
    ex_min_vid = f"{ex_prefix} --min_vid 2"
    ex_tags = f"{ex_prefix} --tags admin,infra"
    ex_vlan_group = f"{ex_prefix} --vlan_group AdminServers"
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update a vlan_group using command line options"
    )
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    optional = parser.add_argument_group(title="OPTIONAL SCRIPT ARGS")
    optional.add_argument(
        "--max_vid",
        dest="max_vid",
        required=False,
        default=None,
        help=f"{help_max_vid} {ex_max_vid}",
    )
    optional.add_argument(
        "--min_vid",
        dest="min_vid",
        required=False,
        default=None,
        help=f"{help_min_vid} {ex_min_vid}",
    )
    optional.add_argument(
        "--description",
        dest="description",
        required=False,
        default=None,
        help=f"{help_description} {ex_description}",
    )
    mandatory.add_argument(
        "--vlan_group",
        dest="vlan_group",
        required=True,
        help=f"{help_vlan_group} {ex_vlan_group}",
    )
    mandatory.add_argument(
        "--tags",
        dest="tags",
        required=False,
        default=None,
        help=f"{help_tags} {ex_tags}",
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
    if cfg.description is not None:
        info["description"] = cfg.description
    if cfg.min_vid is not None:
        info["min_vid"] = cfg.min_vid
    if cfg.max_vid is not None:
        info["max_vid"] = cfg.max_vid
    if cfg.tags is not None:
        info["tags"] = cfg.tags.split(",")
    return info


cfg = get_parser()
netbox_obj = netbox()
vlan_group = VlanGroup(netbox_obj, get_info())
vlan_group.create_or_update()
