#!/usr/bin/env python3
"""
Name: ip_choices_print.py
Description: Display choices associated with endpoint ipam.ip_addresses
"""
from netbox_tools.common import netbox


def get_fmt():
    """
    return a format string
    """
    return "{key:<15} {valid_values:<65}"


def print_header():
    """
    print column header labels
    """
    print(get_fmt().format(key="key", valid_values="valid_values"))
    print(get_fmt().format(key="-" * 15, valid_values="-" * 65))


def print_choices(nb):
    """
    print column values
    """
    items = nb.ipam.ip_addresses.choices()
    for item in items:
        choices_list = []
        for item_dict in items[item]:
            choices_list.append(item_dict["value"])
        print(get_fmt().format(key=item, valid_values=", ".join(choices_list)))


netbox_obj = netbox()
print_header()
print_choices(netbox_obj)
