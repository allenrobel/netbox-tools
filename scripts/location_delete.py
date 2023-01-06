#!/usr/bin/env python3
"""
Name: location_delete.py
Description: Delete location ``--location`` from netbox
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.location import Location

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_location = "Name of the location to delete."

    ex_prefix = " Example: "
    ex_location = f"{ex_prefix} --location mylocation"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Delete location --location from netbox"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--location",
        dest="location",
        required=True,
        help=f"{help_location} {ex_location}",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary containing args expected by Location
    """
    info = {}
    info["name"] = cfg.location
    return info


cfg = get_parser()
nb = netbox()
l = Location(nb, get_info())
l.delete()
