#!/usr/bin/env python3
"""
Name: interface_print.py
Description: Display interface information for ``--device`` ``--interface``
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
    help_detail = "Optional. If present, print detailed info about device."
    help_device = "Name of the device on which interface resides."
    help_interface = "Name of the interface."

    ex_prefix = "Example: "
    ex_detail = f"{ex_prefix} --detail"
    ex_device = f"{ex_prefix} --device leaf_3"
    ex_interface = f"{ex_prefix} --interface mgmt0"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Print information about an interfaces"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    default = parser.add_argument_group(title="DEFAULT SCRIPT ARGS")

    default.add_argument(
        "--detail",
        dest="detail",
        required=False,
        default=False,
        action="store_true",
        help=f"{help_detail} {ex_detail}",
    )
    mandatory.add_argument(
        "--device", dest="device", required=True, help=f"{help_device} {ex_device}"
    )
    mandatory.add_argument(
        "--interface",
        dest="interface",
        required=True,
        help=f"{help_interface} {ex_interface}",
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


def get_interface():
    """
    return device_type object associated with model
    """
    result = netbox_obj.dcim.interfaces.get(device=cfg.device, name=cfg.interface)
    if result is None:
        log(
            f"Device {cfg.device} interface {cfg.interface} does not exist at",
            f"{netbox_obj.base_url}",
        )
        sys.exit(1)
    return result


def print_detail():
    """
    print json returned by Netbox for the interface object
    """
    pretty = json.dumps(dict(interface_obj), indent=4, sort_keys=True)
    print(pretty)


def print_headers():
    """
    print table headers
    """
    print(
        FMT.format(
            "id",
            "device_name",
            "interface",
            "mac_address",
            "type",
            "enabled",
            "mgmt_only",
        )
    )
    print(
        FMT.format(
            "-" * 5,
            "-" * 20,
            "-" * 15,
            "-" * 17,
            "-" * 15,
            "-" * 7,
            "-" * 9
        )
    )


cfg = get_parser()
netbox_obj = netbox()
interface_obj = get_interface()

FMT = "{:>5} {:<20} {:<15} {:<17} {:<15} {:<7} {:<9}"

if cfg.detail:
    print_detail()
else:
    print_headers()
    print(
        FMT.format(
            interface_obj.id,
            interface_obj.device.name,
            interface_obj.name,
            str(interface_obj.mac_address),
            interface_obj.type.value,
            str(interface_obj.enabled),
            str(interface_obj.mgmt_only),
        )
    )
