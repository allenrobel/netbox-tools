#!/usr/bin/env python3
"""
Name: ipam_addresses_print.py
Description: Display all ip addresses
"""
import sys
from netbox_tools.common import netbox


def get_fmt():
    """
    return a format string
    """
    return "{:>5} {:<18} {:<18} {:>6} {:<30}"


def print_ip_addresses():
    """
    print column values
    """
    items = nb.ipam.ip_addresses.all()
    if items is None:
        sys.exit(0)
    fmt = get_fmt()
    for item in items:
        if "device" in dict(item.assigned_object):
            print(
                fmt.format(
                    item.id,
                    item.address,
                    item.assigned_object.device.name,
                    "device",
                    item.description,
                )
            )
        elif "virtual_machine" in dict(item.assigned_object):
            print(
                fmt.format(
                    item.id,
                    item.address,
                    item.assigned_object.virtual_machine.name,
                    "vm",
                    item.description,
                )
            )
        else:
            print(
                fmt.format(
                    item.id,
                    item.address,
                    "na",
                    "na",
                    item.description,
                )
            )


def print_headers():
    """
    print column headers
    """
    fmt = get_fmt()
    print(fmt.format("id", "address", "name", "type", "description"))
    print(fmt.format("-" * 5, "-" * 18, "-" * 18, "-" * 6, "-" * 30))


nb = netbox()
print_headers()
print_ip_addresses()
