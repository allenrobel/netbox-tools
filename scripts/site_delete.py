#!/usr/bin/env python3
"""
Name: site_delete.py
Description: Delete Netbox site ``--site``
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.site import Site

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_site = "Name of the site to delete."

    ex_prefix = " Example: "
    ex_site = f"{ex_prefix} --site mysite"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Delete Netbox site ``--site`"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    mandatory.add_argument(
        "--site", dest="site", required=True, help=f"{help_site} {ex_site}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary containing parameters expected by Site
    """
    info = {}
    info["name"] = cfg.site
    return info


cfg = get_parser()
nb = netbox()
d = Site(nb, get_info())
d.delete()
