#!/usr/bin/env python3
"""
Name: device_print.py
Description: Print information about a device
"""
import argparse
from inspect import stack
import sys
import json
from netbox_tools.common import netbox

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_name = "Name of device to retrieve."
    help_detail = "Optional. If present, print detailed info about device."

    ex_prefix = "Example: "
    ex_name = f"{ex_prefix} --name leaf_3"
    ex_detail = f"{ex_prefix} --detail"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Print information about a device"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    default = parser.add_argument_group(title="DEFAULT SCRIPT ARGS")

    mandatory.add_argument(
        "--name", dest="name", required=True, help=f"{help_name} {ex_name}"
    )
    default.add_argument(
        "--detail",
        dest="detail",
        required=False,
        default=False,
        action="store_true",
        help=f"{help_detail} {ex_detail}",
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


def get_device():
    """
    return device object associated with --name
    """
    device = netbox_obj.dcim.devices.get(name=cfg.name)
    if device is None:
        log(f"Device {cfg.name} does not exist at {netbox_obj.base_url}.")
        sys.exit(1)
    return device


def print_detail():
    """
    print raw json returned by Netbox for device_obj
    """
    pretty = json.dumps(dict(device_obj), indent=4, sort_keys=True)
    print(pretty)


def print_headers():
    """
    print table headers
    """
    print(FMT.format("id", "device_name", "comments"))
    print(FMT.format("-" * 5, "-" * 20, "-" * 30))


FMT = "{:>5} {:<20} {:<30}"

cfg = get_parser()
netbox_obj = netbox()
device_obj = get_device()
if cfg.detail:
    print_detail()
else:
    print_headers()
    print(FMT.format(device_obj.id, device_obj.name, device_obj.comments))
