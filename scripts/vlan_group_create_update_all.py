#!/usr/bin/env python3
"""
Name: vlan_group_create_update_all.py
Description: Create/update vlan_groups defined in ``--yaml``
"""
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.vlan_group import VlanGroup

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing VlanGroup information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./vlans.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update vlan_groups defined in ``--yaml``"
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
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
for key in info["vlan_groups"]:
    vlan_group = VlanGroup(netbox_obj, info["vlan_groups"][key])
    vlan_group.create_or_update()
