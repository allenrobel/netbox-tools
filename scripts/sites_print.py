#!/usr/bin/env python3
"""
Name: sites_print.py
Description: Display information about all Netbox sites
"""
import argparse
import sys
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display information about all Netbox sites"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )
    return parser.parse_args()


def get_fmt():
    """
    return a format string
    """
    fmt = "{id:>5} {name:<15} {device_count:>12} {rack_count:>12} {prefix_count:>12} {status:<10}"
    fmt += " {description:<30}"
    return fmt


def print_headers():
    """
    print column headers
    """
    print(
        get_fmt().format(
            id="id",
            name="name",
            device_count="device_count",
            rack_count="rack_count",
            prefix_count="prefix_count",
            status="status",
            description="description",
        )
    )
    print(
        get_fmt().format(
            id="-" * 5,
            name="-" * 15,
            device_count="-" * 12,
            rack_count="-" * 12,
            prefix_count="-" * 12,
            status="-" * 10,
            description="-" * 30,
        )
    )


def print_values():
    """
    print column values (site info)
    """
    sites = nb.dcim.sites.all()
    if sites is None:
        sys.exit(0)
    for site in sites:
        print(
            get_fmt().format(
                id=site.id,
                name=site.name,
                device_count=site.device_count,
                rack_count=site.rack_count,
                prefix_count=site.prefix_count,
                status=site.status.value,
                description=site.description,
            )
        )


cfg = get_parser()
nb = netbox()
print_headers()
print_values()
