#!/usr/bin/env python3
"""
Name: role_create_update_all.py
Description: Create/update Netbox device roles defined in ``--yaml``

If the roles already exist in netbox, they will be updated with the current information
in the YAML file.

If the roles do not already exist in netbox, they will be created

Example YAML file is given below.

# device role color choices (use RGB values as the color: field value)
# 009688 : Teal
# 4caf50 : Green
# 2196f3 : Blue
# 9c27b0 : Purple
# ffeb3b : Yellow
# ff9800 : Orange
# f44336 : Red
# c0c0c0 : Light Gray
# 9e9e9e : Medium Gray
# 607d8b : Dark Gray

# device_roles mandatory fields:
#   - name
#   - color
---
device_roles:
  leaf:
    name: leaf
    color: 009688
    description: leaf switches
  spine:
    name: spine
    color: 9c27b0
    description: spine switches
  border_gateway:
    name: border_gateway
    color: 4caf50
    description: spine switches
"""
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.role import Role

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing device_roles"

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./info.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update Netbox device roles defined in ``--yaml``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=f"{help_yaml} {ex_yaml}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


cfg = get_parser()
nb = netbox()
info = load_yaml(cfg.yaml)
for key in info["device_roles"]:
    r = Role(nb, info["device_roles"][key])
    r.create_or_update()
