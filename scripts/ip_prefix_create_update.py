#!/usr/bin/env python3
"""
Name: ip_prefix_create_update.py
Description: Create/update an ip prefix using command line options
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.ip_prefix import IpPrefix

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_description = "Optional. Quoted free-form description for this prefix"
    help_prefix = "Prefix to create"
    help_site = "Optional. Site in which prefix will be used"
    help_status = (
        "Optional. Status of the ip prefix (container, active, reserved, deprecated)"
    )

    _ex_prefix_ = " Example: "
    ex_description = f'{_ex_prefix_} --description "this is a description"'
    ex_prefix = f"{_ex_prefix_} --prefix 192.168.1.0/24"
    ex_site = f"{_ex_prefix_} --site SJC03-1-155"
    ex_status = f"{_ex_prefix_} --status active"

    parser = argparse.ArgumentParser(description="DESCRIPTION: Netbox: Add a prefix")

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    optional = parser.add_argument_group(title="OPTIONAL SCRIPT ARGS")

    optional.add_argument(
        "--description",
        dest="description",
        required=False,
        default=None,
        help=help_description + ex_description,
    )

    optional.add_argument(
        "--site", dest="site", required=False, default=None, help=help_site + ex_site
    )

    mandatory.add_argument(
        "--prefix", dest="prefix", required=True, help=help_prefix + ex_prefix
    )

    optional.add_argument(
        "--status",
        dest="status",
        required=False,
        default=None,
        help=help_status + ex_status,
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


cfg = get_parser()
nb = netbox()

info = {}
info["prefix"] = cfg.prefix
if cfg.description is not None:
    info["description"] = cfg.description
if cfg.status is not None:
    info["status"] = cfg.status
if cfg.site is not None:
    info["site"] = cfg.site

p = IpPrefix(nb, info)
p.create_or_update()
