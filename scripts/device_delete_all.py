#!/usr/bin/env python3
"""
Name: device_create_all.py
Summary: Delete all devices contained in the YAML file pointed to with --yaml
Description: Delete all devices in YAML file

Be careful!  This will not ask for confirmation.

"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.common import load_yaml
from netbox_tools.device import Device

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "Name of yaml file containing devices to delete."

    ex_prefix = " Example: "
    ex_yaml = f"{ex_prefix} --yaml /path/to/my.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Delete all devices in YAML file"
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
for key in info["devices"]:
    device_obj = Device(netbox_obj, info["devices"][key])
    device_obj.delete()
