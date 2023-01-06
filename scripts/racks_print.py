#!/usr/bin/env python3
"""
Name: racks_print.py
Description: Display information about all racks
"""
import argparse
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display information about all racks"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_racks():
    """
    return all rack objects
    """
    return nb.dcim.racks.all()


def print_headers():
    """
    print column headers
    """
    print(FMT.format(id="id", name="name", site="site"))
    print(FMT.format(id="-" * 5, name="-" * 15, site="-" * 15))


cfg = get_parser()
nb = netbox()
racks = get_racks()

FMT = "{id:>5} {name:>15} {site:>15}"

print_headers()
for rack in racks:
    print(FMT.format(rack.id, rack.name, rack.site.name))
