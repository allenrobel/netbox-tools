#!/usr/bin/env python3
"""
Name: console_server_ports_print.py
Description: Display information about all console_server_ports
"""
import argparse
from netbox_tools.common import netbox, get_console_server_ports

OUR_VERSION = 102


def get_parser():
    """
    return an argparse parser object
    """
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display information about all console_server_ports"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def print_headers():
    """
    print table headers
    """
    print(FMT.format("id", "device", "port", "description", "tags"))
    print(FMT.format("-" * 4, "-" * 15, "-" * 6, "-" * 30, "-" * 40))


def get_tag_names(tags_list):
    """
    return a list of tag names associated with the console server port
    """
    tag_names = []
    for tag_record in tags_list:
        tag_dict = dict(tag_record)
        tag_names.append(tag_dict["name"])
    return tag_names


FMT = "{:>4} {:<15} {:<6} {:<30} {:<40}"

cfg = get_parser()
netbox_obj = netbox()

console_server_ports = get_console_server_ports(netbox_obj)
print_headers()
for console_server_port in console_server_ports:
    print(
        FMT.format(
            console_server_port.id,
            console_server_port.device.name,
            console_server_port.name,
            console_server_port.description,
            ",".join(get_tag_names(console_server_port.tags)),
        )
    )
