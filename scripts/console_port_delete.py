#!/usr/bin/env python3
"""
Name: console_port_delete.py
Description: Delete console_port --port from netbox
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.console_port import ConsolePort

OUR_VERSION = 101


def get_parser():
    """
    return an argparse parser object
    """
    help_device = "Device containing the console_port to delete."
    help_port = "Name of the console_port to delete."

    ex_prefix = " Example: "
    ex_device = f"{ex_prefix} --device mydevice"
    ex_port = f"{ex_prefix} --port myconsole_port"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Delete a console_port"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--device", dest="device", required=True, help=help_device + ex_device
    )
    mandatory.add_argument(
        "--port", dest="port", required=True, help=help_port + ex_port
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary with key/values that ConsolePort expects
    """
    info = {}
    info["port"] = cfg.port
    info["device"] = cfg.device
    return info


cfg = get_parser()
netbox_obj = netbox()
c = ConsolePort(netbox_obj, get_info())
c.delete()
