#!/usr/bin/env python3
"""
Name: rack_print.py
Description: Display information about ``--rack``
"""
import argparse
import json
import sys
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_detail = "Optional. If present, print detailed info about --rack."
    help_rack = "Name of the rack."

    ex_prefix = "Example: "
    ex_detail = f"{ex_prefix} --detail"
    ex_rack = f"{ex_prefix} --rack V009"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display information about ``--rack``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    default = parser.add_argument_group(title="DEFAULT SCRIPT ARGS")

    default.add_argument(
        "--detail",
        dest="detail",
        required=False,
        default=False,
        action="store_true",
        help=f"{help_detail} {ex_detail}",
    )
    mandatory.add_argument(
        "--rack", dest="rack", required=True, help=f"{help_rack} {ex_rack}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def error():
    """
    print a helpful error and exit
    """
    racks = []
    items = nb.dcim.racks.all()
    for item in items:
        racks.append(item.name)
    print(f"Rack {cfg.rack} does not exist in netbox.  Valid racks: {', '.join(racks)}")
    sys.exit(1)


def get_rack():
    """
    return rack object matching cfg.rack
    If rack is not found, error and exit.
    """
    rack_obj = nb.dcim.racks.get(name=cfg.rack)
    if rack_obj is None:
        error()
    return rack_obj


def print_detail():
    """
    print detailed info about a rack
    """
    pretty = json.dumps(dict(rack), indent=4, sort_keys=True)
    print(pretty)


def print_headers():
    """
    print column headers
    """
    print(FMT.format(id="id", name="name", site="site"))
    print(FMT.format(id="-" * 5, name="-" * 15, site="-" * 15))


cfg = get_parser()
nb = netbox()
rack = get_rack()

FMT = "{id:>5} {name:>15} {site:>15}"

if cfg.detail:
    print_detail()
    sys.exit(0)

print_headers()
print(FMT.format(id=rack.id, name=rack.name, site=rack.site.name))
