#!/usr/bin/env python3
"""
Name: role_delete.py
Description: Delete Netbox device role ``--role``
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.role import Role

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_role = "Name of the role to delete."

    ex_prefix = " Example: "
    ex_role = f"{ex_prefix} --role myrole"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Delete Netbox device role ``--role``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--role", dest="role", required=True, help=f"{help_role} {ex_role}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary containing args expected by Role
    """
    info = {}
    info["name"] = cfg.role
    return info


cfg = get_parser()
nb = netbox()
role_obj = Role(nb, get_info())
role_obj.delete()
