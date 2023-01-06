#!/usr/bin/env python3
"""
Name: site_print.py
Description: Display information about ``--site``
"""
import argparse
import json
import sys
from inspect import stack
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_detail = "Optional. If present, print detailed info about role."
    help_site = "Retrieve information for site"

    ex_prefix = "Example: "
    ex_detail = f"{ex_prefix} --detail"
    ex_site = f"{ex_prefix} --site fabric_1"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Print information about a site"
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
        "--site", dest="site", required=True, help=f"{help_site} {ex_site}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def log(*args):
    """
    simple logger
    """
    print(f"{stack()[1].function}(v{OUR_VERSION}): {' '.join(args)}")


def error():
    """
    print a helpful error message and exit
    """
    sites = []
    items = nb.dcim.sites.all()
    for item in items:
        sites.append(item.name)
    log(f"site {cfg.site} does not exist in netbox.  Valid sites: {', '.join(sites)}")
    sys.exit(1)


def get_fmt():
    """
    return a format string
    """
    fmt = "{id:>5} {name:<15} {device_count:>12} {rack_count:>12} {prefix_count:>12} {status:<10}"
    fmt += " {description:<30}"
    return fmt


def get_site():
    """
    Return a site object matching the user's query, if any.
    If no match is found, exit with error.
    """
    site = nb.dcim.sites.get(name=cfg.site)
    if site is None:
        error()
    return site


def print_detail(site):
    """
    print detailed info about site
    """
    pretty = json.dumps(dict(site), indent=4, sort_keys=True)
    print(pretty)


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


def print_values(site):
    """
    print column values (site info)
    """
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
site_obj = get_site()
if cfg.detail:
    print_detail(site_obj)
    sys.exit(0)
print_headers()
print_values(site_obj)
