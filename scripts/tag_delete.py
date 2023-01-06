#!/usr/bin/env python3
"""
Name: tag_delete.py
Description: Delete Netbox tag ``--tag``
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.tag import Tag

OUR_VERSION = 106


def get_parser():
    """
    return an argparse parser object
    """
    help_tag = "Name of the tag to delete."

    ex_prefix = " Example: "
    ex_tag = f"{ex_prefix} --tag infra"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Delete Netbox tag ``--tag``"
    )
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    mandatory.add_argument(
        "--tag", dest="tag", required=True, help=f"{help_tag} {ex_tag}"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )
    return parser.parse_args()


def get_info():
    """
    Return dictionary containing parameters expected by Tag
    """
    info = {}
    info["name"] = cfg.tag
    return info


cfg = get_parser()
nb = netbox()
tag_obj = Tag(nb, get_info())
tag_obj.delete()
