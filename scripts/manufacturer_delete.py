#!/usr/bin/env python3
"""
Name: manufacturer_delete.py
Description: Delete Netbox manufacturer ``--manufacturer``
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.manufacturer import Manufacturer

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_manufacturer = "Name of the manufacturer to delete."

    ex_prefix = " Example: "
    ex_manufacturer = f"{ex_prefix} --manufacturer mymanufacturer"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Delete Netbox manufacturer ``--manufacturer``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--manufacturer",
        dest="manufacturer",
        required=True,
        help=f"{help_manufacturer} {ex_manufacturer}",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary containing args expected by Manufacturer
    """
    info = {}
    info["name"] = cfg.manufacturer
    return info


cfg = get_parser()
nb = netbox()
d = Manufacturer(nb, get_info())
d.delete()
