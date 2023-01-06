#!/usr/bin/env python3
"""
Name: role_print.py
Description: Display information about device role ``--role``
"""
import argparse
import json
import sys
from netbox_tools.common import netbox
from netbox_tools.colors import rgb_to_color

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_detail = "Optional. If present, print detailed info about role."
    help_role = "Role for the device."

    ex_prefix = "Example: "
    ex_detail = f"{ex_prefix} --detail"
    ex_role = f"{ex_prefix} --role leaf"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display information about device role ``--role``"
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
        "--role", dest="role", required=True, help=f"{help_role} {ex_role}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def error():
    """
    exit with a helpful error message
    """
    roles = []
    items = nb.dcim.device_roles.all()
    for item in items:
        roles.append(item.name)
    print(f"Role {cfg.role} does not exist in netbox.  Valid roles: {', '.join(roles)}")
    sys.exit(1)


def get_device_role():
    """
    Return a device_role object matching the role name in cfg.role
    If the device_role does not exist exit with an error.
    """
    role_obj = nb.dcim.device_roles.get(name=cfg.role)
    if role_obj is None:
        error()
    return role_obj


def print_detail():
    """
    Print detailed info about the role
    """
    pretty = json.dumps(dict(role), indent=4, sort_keys=True)
    print(pretty)


def print_headers():
    """
    print column headers
    """
    print(
        FMT.format(
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
        FMT.format(
            id="-" * 5,
            role_name="-" * 15,
            device_count="-" * 12,
            rgb="-" * 6,
            color="-" * 15,
            vm_role="-" * 7,
            description="-" * 30,
        )
    )


cfg = get_parser()
nb = netbox()
role = get_device_role()

FMT = "{id:>5} {role_name:<15} {device_count:>12} {rgb:<6} {color:<15} {vm_role:<7}"
FMT += " {description:<30}"

if cfg.detail:
    print_detail()
    sys.exit(0)

print_headers()
print(
    FMT.format(
        id=role.id,
        role_name=role.name,
        device_count=role.device_count,
        rgb=role.color,
        color=rgb_to_color(role.color),
        vm_role=role.vm_role,
        description=role.description,
    )
)
