#!/usr/bin/env python3
"""
Name: vlan_group_print.py
Description: Display information about Netbox vlan_group ``--vlan_group``
"""
import argparse
from inspect import stack
import json
import sys
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_detail = "Optional. If present, print detailed info about VlanGroup."
    help_vlan_group = "Name of the VlanGroup."

    ex_prefix = "Example: "
    ex_detail = f"{ex_prefix} --detail"
    ex_vlan_group = "{ex_prefix} --vlan_group AdminServers"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display information about Netbox vlan_group ``--vlan_group``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    default = parser.add_argument_group(title="DEFAULT SCRIPT ARGS")

    default.add_argument(
        "--detail",
        dest="detail",
        required=False,
        default=False,
        action="store_true",
        help=f"{help_detail} {ex_detail}",
    )
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


def log(*args):
    """
    simple logger
    """
    print(f"{stack()[1].function}(v{OUR_VERSION}): {' '.join(args)}")


def error(netbox_object):
    """
    Print a helpful error message and exit.
    """
    vlan_groups = []
    items = netbox_object.ipam.vlan_groups.all()
    for item in items:
        vlan_groups.append(item.name)
    msg = f"vlan_group {cfg.vlan_group} does not exist in netbox."
    msg += f" Valid vlan_groups: {', '.join(vlan_groups)}"
    log(msg)
    sys.exit(1)


def get_vlan_group(netbox_object):
    """
    Return a vlan_group object matching user's search.
    If object does not exist, call error()
    """
    vlan_group = netbox_object.ipam.vlan_groups.get(name=cfg.vlan_group)
    if vlan_group is None:
        error(netbox_object)
    return vlan_group


def print_detail(vlan_group):
    """
    Print detailed info about vlan_group
    """
    pretty = json.dumps(dict(vlan_group), indent=4, sort_keys=True)
    print(pretty)


def print_headers():
    """
    print column headers
    """
    print(
        get_fmt().format(
            id="id",
            name="name",
            min_vid="min_vid",
            max_vid="max_vid",
            description="description",
        )
    )
    print(
        get_fmt().format(
            id="-" * 5,
            name="-" * 15,
            min_vid="-" * 7,
            max_vid="-" * 7,
            description="-" * 25,
        )
    )


def print_values(vlan_group):
    """
    print column values
    """
    print(
        get_fmt().format(
            id=vlan_group.id,
            name=vlan_group.name,
            min_vid=vlan_group.min_vid,
            max_vid=vlan_group.max_vid,
            description=str(vlan_group.description),
        )
    )


def get_fmt():
    """
    return a format string
    """
    return "{id:>5} {name:<15} {min_vid:>7} {max_vid:>7} {description:<25}"


cfg = get_parser()
netbox_obj = netbox()
vlan_group_obj = get_vlan_group(netbox_obj)

if cfg.detail:
    print_detail(vlan_group_obj)
    sys.exit(0)

print_headers()
print_values(vlan_group_obj)
