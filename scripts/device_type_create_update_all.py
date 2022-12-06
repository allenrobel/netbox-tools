#!/usr/bin/env python3
"""
Name: device_type_create_update_all.py
Description: Create/update device types from information in a YAML file
"""
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.device_type import DeviceType

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing device type information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./device_types.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create or update Netbox device types"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=f"{help_yaml} {ex_yaml}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s v{OUR_VERSION}"
    )

    return parser.parse_args()


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
for key in info["device_types"]:
    device_type = DeviceType(netbox_obj, info["device_types"][key])
    device_type.create_or_update()
