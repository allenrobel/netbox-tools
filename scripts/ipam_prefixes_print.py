#!/usr/bin/env python3
"""
Name: ipam_prefixes_print.py
Description: Display all ip prefixes
"""
import sys
from netbox_tools.common import netbox


def get_fmt():
    """
    return a format string
    """
    return "{id:>6} {prefix:<18} {status:<10} {site:<15} {vrf:<10} {description:<25}"


def print_ip_prefixes():
    """
    print column values
    """
    items = nb.ipam.prefixes.all()
    if items is None:
        print("print_ip_prefixes: exiting. no prefixes found in netbox")
        sys.exit(0)
    fmt = get_fmt()
    for item in items:
        iid = item.id
        prefix = item.prefix
        status = item.status.label
        if item.site is None:
            site = "na"
        else:
            site = item.site.name
        if item.vrf is None:
            vrf = "na"
        else:
            vrf = item.vrf
        description = item.description
        print(
            fmt.format(
                id=iid,
                prefix=prefix,
                status=status,
                site=site,
                vrf=vrf,
                description=description,
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
            prefix="prefix",
            status="status",
            site="site",
            vrf="vrf",
            description="description",
        )
    )
    print(
        fmt.format(
            id="-" * 6,
            prefix="-" * 18,
            status="-" * 10,
            site="-" * 15,
            vrf="-" * 10,
            description="-" * 25,
        )
    )


nb = netbox()
print_headers()
print_ip_prefixes()
