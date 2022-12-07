#!/usr/bin/env python3
"""
Name: interface_create_update_all.py
Description: Create/update all ip prefixes defined in ``--yaml``
"""
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.interface import Interface

OUR_VERSION = 102


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file in which prefix information can be found."

    ex_prefix_ = " Example: "
    ex_yaml = f"{ex_prefix_} --yaml ./info.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Create or update all interfaces"
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
info = load_yaml(cfg.yaml)
netbox_obj = netbox()
print("---")
for key in info["interfaces"]:
    i = Interface(netbox_obj, info["interfaces"][key])
    i.create_or_update()
