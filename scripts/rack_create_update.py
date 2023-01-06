#!/usr/bin/env python3
"""
Name: rack_create_update.py
Description: Create/update Netbox rack using command line options
Example Usage:

./rack_create_update.py \
    --rack A001 \
    --location row-a \
    --site volcano \
    --u_height 48 \
    --comments "a comment" \
    --tags infra,admin
"""
import argparse
import re
from netbox_tools.common import netbox
from netbox_tools.rack import Rack

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_comments = "Free-form comment for --rack"
    help_location = "Location of --rack"
    help_rack = "Rack name"
    help_site = "Site containing --rack"
    help_tags = "Comma-separated list of tags (no spaces) to apply to this rack."
    help_tags += " All tags must already exist in Netbox."
    help_u_height = "Height of --rack in RU (rack units)"

    ex_prefix = "Example: "
    ex_comments = f'{ex_prefix} --comments "this is a rack comment"'
    ex_location = f"{ex_prefix} --location row-c"
    ex_rack = f"{ex_prefix} --rack C004"
    ex_site = f"{ex_prefix} --site mysite"
    ex_tags = f"{ex_prefix} --tags admin,infra"
    ex_u_height = f"{ex_prefix} --u_height 48"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update a Netbox rack using command line options"
    )
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    optional = parser.add_argument_group(title="OPTIONAL SCRIPT ARGS")

    optional.add_argument(
        "--comments",
        dest="comments",
        required=False,
        default=None,
        help=f"{help_comments} {ex_comments}",
    )
    mandatory.add_argument(
        "--location",
        dest="location",
        required=True,
        help=f"{help_location} {ex_location}",
    )
    mandatory.add_argument(
        "--rack", dest="rack", required=True, help=f"{help_rack} {ex_rack}"
    )
    mandatory.add_argument(
        "--site", dest="site", required=True, help=f"{help_site} {ex_site}"
    )
    optional.add_argument(
        "--tags",
        dest="tags",
        required=False,
        default=None,
        help=f"{help_tags} {ex_tags}",
    )
    optional.add_argument(
        "--u_height",
        dest="u_height",
        required=False,
        default=None,
        help=f"{help_u_height} {ex_u_height}",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary containing args expected by Rack
    """
    info = {}
    info["name"] = cfg.rack
    info["location"] = cfg.location
    info["site"] = cfg.site
    if cfg.comments is not None:
        info["comments"] = cfg.comments
    if cfg.u_height is not None:
        info["u_height"] = cfg.u_height
    if cfg.tags is not None:
        info["tags"] = re.split(",", cfg.tags)
    return info


cfg = get_parser()
nb = netbox()
rack = Rack(nb, get_info())
rack.create_or_update()
