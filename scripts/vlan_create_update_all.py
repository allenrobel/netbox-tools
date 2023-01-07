#!/usr/bin/env python3
"""
Name: vlan_create_update_all.py
Description: Create/update vlans defined in ``--yaml``
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import netbox, load_yaml
from netbox_tools.vlan import Vlan

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing Vlan information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./vlans.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update vlans defined in ``--yaml``"
    )
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=f"{help_yaml} {ex_yaml}"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )
    return parser.parse_args()


def log(*args):
    """
    simple logger
    """
    print(f"{stack()[1].function}(v{OUR_VERSION}): {' '.join(args)}")


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
if "vlans" not in info:
    log(f"Exiting. No vlans to process in {cfg.yaml}")
    sys.exit(1)
for key in info["vlans"]:
    vlan = Vlan(netbox_obj, info["vlans"][key])
    vlan.create_or_update()
