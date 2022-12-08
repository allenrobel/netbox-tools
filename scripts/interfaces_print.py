#!/usr/bin/env python3
"""
Name: interfaces_print.py
Description: Display information about all interfaces
"""
import argparse
import sys
from netbox_tools.common import netbox

OUR_VERSION = 102


def get_parser():
    """
    return an argparse parser object
    """
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Print information about all interfaces"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s v{OUR_VERSION}"
    )

    return parser.parse_args()


def get_fmt():
    """
    return the output format string
    """
    return "{:>5} {:<20} {:<18} {:<17} {:<15} {:<7} {:<9}"


def print_headers():
    """
    print the table headers
    """
    fmt = get_fmt()
    print(
        fmt.format(
            "id",
            "device_name",
            "interface",
            "mac_address",
            "type",
            "enabled",
            "mgmt_only",
        )
    )
    print(fmt.format("-" * 5, "-" * 20, "-" * 18, "-" * 17, "-" * 15, "-" * 7, "-" * 9))


def print_items(items):
    """
    print the table items
    """
    fmt = get_fmt()
    for item in items:
        print(
            fmt.format(
                item.id,
                item.device.name,
                item.name,
                str(item.mac_address),
                item.type.value,
                str(item.enabled),
                str(item.mgmt_only),
            )
        )


def get_interfaces():
    """
    return all Netbox interface objects
    """
    result = netbox_obj.dcim.interfaces.all()
    if result is None:
        print("Exiting: no interfaces")
        sys.exit(1)
    return result


netbox_obj = netbox()
cfg = get_parser()
response = get_interfaces()
print_headers()
print_items(response)
