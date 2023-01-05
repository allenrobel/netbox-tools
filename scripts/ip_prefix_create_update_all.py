#!/usr/bin/env python3
"""
Name: ip_prefix_create_update_all.py
Description: Create/update all ip prefixes defined in ``--yaml``
"""
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.ip_prefix import IpPrefix

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file in which prefix information can be found."

    ex_prefix = " Example: "
    ex_yaml = f"{ex_prefix} --yaml ./info.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Create or update all ip prefixes"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=help_yaml + ex_yaml
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


cfg = get_parser()
info = load_yaml(cfg.yaml)
nb = netbox()
print("---")
for key in info["prefixes"]:
    p = IpPrefix(nb, info["prefixes"][key])
    p.create_or_update()
