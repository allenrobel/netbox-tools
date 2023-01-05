#!/usr/bin/env python3
"""
Name: ip_choices_print.py
Description: Display choices associated with endpoint ipam.ip_addresses
"""
from netbox_tools.common import netbox


def print_header():
    """
    print column header labels
    """
    print(FMT.format("key", "valid_values"))
    print(FMT.format("-" * 15, "-" * 65))


def print_choices(items):
    """
    print column values
    """
    for item in items:
        choices_list = []
        for item_dict in items[item]:
            choices_list.append(item_dict["value"])
        print(FMT.format(item, ", ".join(choices_list)))


nb = netbox()

choices = nb.ipam.ip_addresses.choices()

FMT = "{:<15} {:<65}"
print_header()
print_choices(choices)
