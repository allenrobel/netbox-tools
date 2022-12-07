#!/usr/bin/env python3
"""
Name: device_type_create_update.py
Description: Create or update a Netbox device type using command line options
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.device_type import DeviceType

OUR_VERSION = 105


def get_parser():
    """
    return an argparse parser object
    """
    help_comments = "Freeform comments for this device type"
    help_manufacturer = "Who makes this device type"
    help_model = "Typically, the product/model number for this device type"
    help_tags = "A comma-separated list of tags for this device type"
    help_tags += " (these must already exist in netbox)"
    ex_prefix = "Example: "
    ex_comments = f"{ex_prefix} --comments '36x40/100G QSFP28 Ethernet Module'"
    ex_manufacturer = f"{ex_prefix} --manufacturer cisco"
    ex_model = f"{ex_prefix} --model N9K-C9336C-FX2"
    ex_tags = f"{ex_prefix} --tags admin,infra"
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create or update a Netbox device type"
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
        "--manufacturer",
        dest="manufacturer",
        required=True,
        help=f"{help_manufacturer} {ex_manufacturer}",
    )

    mandatory.add_argument(
        "--model", dest="model", required=True, help=f"{help_model} {ex_model}"
    )

    optional.add_argument(
        "--tags",
        dest="tags",
        required=False,
        default=None,
        help=f"{help_tags} {ex_tags}",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s v{OUR_VERSION}"
    )

    return parser.parse_args()


cfg = get_parser()
netbox_obj = netbox()

info = {}
info["manufacturer"] = cfg.manufacturer
info["model"] = cfg.model
if cfg.comments is not None:
    info["comments"] = cfg.comments
if cfg.tags is not None:
    info["tags"] = cfg.tags.split(",")

d = DeviceType(netbox_obj, info)
d.create_or_update()
