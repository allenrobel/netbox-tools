#!/usr/bin/env python3
"""
Name: device_choices_print.py
Description: Display choices associated with Netbox endpoint dcim.devices
"""
import argparse
from netbox_tools.common import netbox

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display choices associated with Netbox endpoint dcim.devices"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s v{OUR_VERSION}"
    )

    return parser.parse_args()


def print_header():
    """
    print table header
    """
    print(FMT.format("key", "valid_values"))
    print(FMT.format("-" * 15, "-" * 65))


def print_choices():
    """
    print table data
    """
    for item in items:
        choices = []
        for item_dict in items[item]:
            choices.append(item_dict["value"])
        print(FMT.format(item, ", ".join(choices)))


netbox_obj = netbox()
cfg = get_parser()

items = netbox_obj.dcim.devices.choices()

FMT = "{:<15} {:<65}"
print_header()
print_choices()
