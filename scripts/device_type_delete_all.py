#!/usr/bin/env python3
"""
Name: device_type_delete_all.py
Summary: Delete all device types contained in the YAML file ``--yaml``

Be careful!  This will not ask for confirmation.

"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.common import load_yaml
from netbox_tools.device_type import DeviceType

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "Name of yaml file containing device types to delete."

    ex_prefix = " Example: "
    ex_yaml = f"{ex_prefix} --yaml /path/to/my.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Delete all device types in YAML file"
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
nb = netbox()
info = load_yaml(cfg.yaml)
for key in info["device_types"]:
    d = DeviceType(nb, info["device_types"][key])
    d.delete()
