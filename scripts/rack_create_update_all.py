#!/usr/bin/env python3
"""
Name: rack_create_update_all.py
Description: Create/update Netbox racks defined in ``--yaml``
"""
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.rack import Rack

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing device type information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./racks.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update Netbox racks defined in ``--yaml`"
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
for key in info["racks"]:
    rack = Rack(nb, info["racks"][key])
    rack.create_or_update()
