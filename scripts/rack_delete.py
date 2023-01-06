#!/usr/bin/env python3
"""
Name: rack_delete.py
Description: Delete Netbox rack ``--rack``
"""
import argparse

from netbox_tools.common import netbox
from netbox_tools.rack import Rack

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_rack = "Name of the rack to delete."

    ex_prefix = " Example: "
    ex_rack = f"{ex_prefix} --rack myrack"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Delete Netbox rack ``--rack``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--rack", dest="rack", required=True, help=f"{help_rack} {ex_rack}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary containing args expected by Rack
    """
    info = {}
    info["name"] = cfg.rack
    return info


cfg = get_parser()
nb = netbox()
d = Rack(nb, get_info())
d.delete()
