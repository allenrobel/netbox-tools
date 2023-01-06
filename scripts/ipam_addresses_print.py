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
    return "{id:>5} {address:<18} {device:<18} {type:>6} {description:<30}"


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
            name = item.assigned_object.device.name
            device_type = "device"
        elif "virtual_machine" in dict(item.assigned_object):
            name = item.assigned_object.virtual_machine.name
            device_type = "vm"
        else:
            name = "na"
            device_type = "na"
        print(
            fmt.format(
                id=item.id,
                address=item.address,
                device=name,
                type=device_type,
                description=item.description,
            )
        )


def print_headers():
    """
    print column headers
    """
    fmt = get_fmt()
    print(
        fmt.format(
            id="id",
            address="address",
            device="name",
            type="type",
            description="description",
        )
    )
    print(
        fmt.format(
            id="-" * 5,
            address="-" * 18,
            device="-" * 18,
            type="-" * 6,
            description="-" * 30,
        )
    )


nb = netbox()
print_headers()
print_ip_addresses()
