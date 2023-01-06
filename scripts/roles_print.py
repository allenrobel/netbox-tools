#!/usr/bin/env python3
"""
Name: roles_print.py
Description: Display information about all Netbox device roles
"""
import argparse
import sys
from netbox_tools.common import netbox
from netbox_tools.colors import rgb_to_color

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display information about all Netbox device roles"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_fmt():
    """
    return a format string
    """
    fmt = "{id:>5} {role_name:<18} {device_count:>12} {rgb:<6} {color:<15} {vm_role:<7}"
    fmt += " {description:<30}"
    return fmt


def print_device_roles():
    """
    print column values
    """
    roles = nb.dcim.device_roles.all()
    if roles is None:
        sys.exit(0)
    fmt = get_fmt()
    for role in roles:
        print(
            fmt.format(
                id=role.id,
                role_name=role.name,
                device_count=role.device_count,
                rgb=role.color,
                color=rgb_to_color(role.color),
                vm_role=role.vm_role,
                description=role.description,
            )
        )


def print_headers():
    """
    print column headers
    """
    fmt = get_fmt()
    print(
        fmt.format(
            id="id",
            role_name="role_name",
            device_count="device_count",
            rgb="rgb",
            color="color",
            vm_role="vm_role",
            description="description",
        )
    )
    print(
        fmt.format(
            id="-" * 5,
            role_name="-" * 18,
            device_count="-" * 12,
            rgb="-" * 6,
            color="-" * 15,
            vm_role="-" * 7,
            description="-" * 30,
        )
    )


cfg = get_parser()
nb = netbox()

print_headers()
print_device_roles()
