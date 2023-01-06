#!/usr/bin/env python3
"""
Name: role_create_update.py
Description: Create/update Netbox device role using command line options
Example Usage:

./role_create_update.py \
    --role leaf \
    --color green_dark \
    --description "leaf switches" \
    --tags ecmp_16,500w

Notes:
   1. --color is currently limited to the set of colors defined in ./lib/netbox_tools/colors.py
   2. --tags must already exist in Netbox
"""
import argparse
import re
from netbox_tools.common import netbox
from netbox_tools.role import Role

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_color = "Color to associate with --role"
    help_description = "Free-form description for --role"
    help_role = "role name"
    help_tags = "Comma-separated list of tags (no spaces) to apply to this role."
    help_tags += " All tags must already exist in Netbox."

    ex_prefix = "Example: "
    ex_color = "f{ex_prefix} --color green"
    ex_description = f"{ex_prefix} --description 'this is a role description'"
    ex_role = "f{ex_prefix} --role C004"
    ex_tags = "f{ex_prefix} --tags admin,infra"
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update Netbox device role using command line options"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    optional = parser.add_argument_group(title="OPTIONAL SCRIPT ARGS")

    mandatory.add_argument(
        "--color", dest="color", required=True, help=f"{help_color} {ex_color}"
    )
    optional.add_argument(
        "--description",
        dest="description",
        required=False,
        default=None,
        help=f"{help_description} {ex_description}",
    )
    mandatory.add_argument(
        "--role", dest="role", required=True, help=f"{help_role} {ex_role}"
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
    return dictionary containing args expected by Role
    """
    info = {}
    info["name"] = cfg.role
    info["color"] = cfg.color
    if cfg.description is not None:
        info["description"] = cfg.description
    if cfg.tags is not None:
        info["tags"] = re.split(",", cfg.tags)
    return info


cfg = get_parser()
nb = netbox()
role = Role(nb, get_info())
role.create_or_update()
