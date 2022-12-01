#!/usr/bin/env python3
"""
Name: console_server_port_create_update.py
Description: Create/update a console server port
Example Usage:
./console_server_port_create_update.py \
    --device ts_1 \
    --port 2003 \
    --description "a special port" \
    --tags admin,infra
"""
import argparse
import re
from netbox_tools.common import netbox
from netbox_tools.console_server_port import ConsoleServerPort

OUR_VERSION = 106


def get_parser():
    """
    return an argparse parser object
    """
    help_description = "Optional. Description of the console_server_port."
    help_device = "Device name to which the console_server_port (--port) will be added."
    help_port = "Console server port to create or update"
    help_tags = "Optional. Comma-separated (no spaces) list of tags "
    help_tags += "to associate with the console server port"

    ex_prefix = " Example: "
    ex_description = (
        f"{ex_prefix} --description 'this is a very special console server port'"
    )
    ex_device = f"{ex_prefix} --device ts_1"
    ex_port = f"{ex_prefix} --port"
    ex_tags = f"{ex_prefix} --tags admin,infra"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Create/update a console server port"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    optional = parser.add_argument_group(title="OPTIONAL SCRIPT ARGS")

    optional.add_argument(
        "--description",
        dest="description",
        required=False,
        default=None,
        help=f"{help_description} {ex_description}",
    )

    mandatory.add_argument(
        "--device", dest="device", required=True, help=f"{help_device} {ex_device}"
    )

    mandatory.add_argument(
        "--port", dest="port", required=True, help=f"{help_port} {ex_port}"
    )

    optional.add_argument(
        "--tags",
        dest="tags",
        required=False,
        default=None,
        help=f"{help_tags} {ex_tags}",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_args():
    """
    Mandatory keys:
       device: name of the device
       port: name of the console port e.g. for Cisco terminal servers: 2005
    Optional keys:
        description: Free-form description for the console server port
        tags: Python list of tags to associate with the console server port
    """
    args = {}
    args["device"] = cfg.device
    args["port"] = cfg.port
    if cfg.description is not None:
        args["description"] = cfg.description
    if cfg.tags is not None:
        args["tags"] = re.split(",", cfg.tags)
    return args


cfg = get_parser()
netbox_obj = netbox()
c = ConsoleServerPort(netbox_obj, get_args())
c.create_or_update()
