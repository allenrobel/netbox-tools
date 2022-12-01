#!/usr/bin/env python3
"""
Name: console_server_port_create_update_all.py
Description: create/update netbox console-server-ports from information in a YAML file.
"""
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.console_server_port import ConsoleServerPort

OUR_VERSION = 102


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing console_server_ports information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./console_server_ports.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: create/update netbox console-server-ports"
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
for key in info["console_server_ports"]:
    console_server_port = ConsoleServerPort(
        netbox_obj,
        info["console_server_ports"][key]
    )
    console_server_port.create_or_update()
