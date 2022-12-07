#!/usr/bin/env python3
"""
Name: device_types_print.py
Description: Display summary information about all device types
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Print summary information about all device types"
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



def get_device_types():
    """
    return all Netbox device types
    """
    try:
        result = nb.dcim.device_types.all()
        return result
    except Exception as _general_exception:
        log(
            "Could not retrieve device types.",
            f"Exception detail: {_general_exception}"
        )
        sys.exit(1)


def print_headers():
    """
    print table headers
    """
    print(FMT.format("id", "name", "device_count", "manufacturer"))
    print(FMT.format("-" * 5, "-" * 15, "-" * 12, "-" * 20))


cfg = get_parser()
nb = netbox()

device_types = get_device_types()
FMT = "{:>5} {:<15} {:>12} {:<20}"
print_headers()
for device_type_obj in device_types:
    print(
        FMT.format(
            device_type_obj.id,
            device_type_obj.model,
            device_type_obj.device_count,
            device_type_obj.manufacturer.name
        )
    )
