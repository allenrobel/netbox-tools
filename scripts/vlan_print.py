#!/usr/bin/env python3
"""
Name: vlan_group_print.py
Description: Display information about Netbox vlan_group ``--vlan_group``
"""
import argparse
from inspect import stack
import json
import sys
import pynetbox
from netbox_tools.common import netbox

OUR_VERSION = 100


def get_parser():
    """
    return an argparse parser object
    """
    help_detail = "Optional. If present, print detailed info about VlanGroup."
    help_vid = "Optional, ID of the vlan to print."
    help_vid += " If not specified, all vlans will be printed."

    ex_prefix = "Example: "
    ex_detail = f"{ex_prefix} --detail"
    ex_vid = "{ex_prefix} --vlan 10"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display information about Netbox vlan ``--vid``"
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
        "--vid",
        dest="vid",
        required=False,
        default=None,
        help=f"{help_vid} {ex_vid}",
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
    vlans = []
    items = netbox_object.ipam.vlans.all()
    for item in items:
        vlans.append(str(item.vid))
    msg = f"vlan ID {cfg.vid} does not exist in netbox."
    msg += f" Valid vlans: {', '.join(vlans)}"
    log(msg)
    sys.exit(1)


def get_vid(netbox_object):
    """
    Return a vlan object matching cfg.vid
    If object does not exist, call error()
    """
    if cfg.vid is None:
        vid = netbox_object.ipam.vlans.all()
    else:
        vid = netbox_object.ipam.vlans.get(vid=cfg.vid)
    if vid is None:
        error(netbox_object)
    return vid


def print_detail(vlans):
    """
    Print detailed info about vlans
    """
    for vlan in vlans:
        pretty = json.dumps(dict(vlan), indent=4, sort_keys=True)
        print(pretty)


def print_headers():
    """
    print column headers
    """
    print(
        get_fmt().format(
            id="id",
            vid="vid",
            name="name",
            site="site",
            description="description",
        )
    )
    print(
        get_fmt().format(
            id="-" * 5,
            vid="-" * 5,
            name="-" * 15,
            site="-" * 15,
            description="-" * 25,
        )
    )


def print_values(vlans):
    """
    print column values
    """
    for vlan in vlans:
        print(
            get_fmt().format(
                id=str(vlan.id),
                vid=str(vlan.vid),
                name=str(vlan.name),
                site=str(vlan.site),
                description=str(vlan.description),
            )
        )


def get_fmt():
    """
    return a format string
    """
    return "{id:>5} {vid:<5} {name:>15} {site:>15} {description:<25}"


cfg = get_parser()
netbox_obj = netbox()
vlan_obj = get_vid(netbox_obj)
# If not of type pynetbox.core.response.RecordSet, convert to a list of one object
# so we can handle everything as a list from this point onward.
# If it IS a RecordSet then we can handle as if it's a list.
if isinstance(vlan_obj, pynetbox.models.ipam.Vlans):
    vlan_obj = [vlan_obj]

if cfg.detail:
    print_detail(vlan_obj)
    sys.exit(0)

print_headers()
print_values(vlan_obj)
