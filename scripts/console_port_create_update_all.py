#!/usr/bin/env python3
"""
Name: console_port_create_update_all.py
Description: Create/update all cables defined in ``--yaml``
"""
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.console_port import ConsolePort

OUR_VERSION = 101


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing console_ports information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./console_ports.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update all cables defined in ``--yaml``"
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
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
for key in info["console_ports"]:
    console_port = ConsolePort(netbox_obj, info["console_ports"][key])
    console_port.create_or_update()
