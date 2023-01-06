#!/usr/bin/env python3
"""
Name: tags_print.py
Description: Display information about all tags
"""
import argparse
from netbox_tools.colors import color
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Display information about all tags"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )
    return parser.parse_args()


def get_fmt():
    """
    return a format string
    """
    return (
        "{id:>5} {name:<15} {tagged_items:>12} {rgb:>6} {color:<10} {description:<30}"
    )


def print_headers():
    """
    print column headers
    """
    print(
        get_fmt().format(
            id="id",
            name="name",
            tagged_items="tagged_items",
            rgb="rgb",
            color="color",
            description="description",
        )
    )
    print(
        get_fmt().format(
            id="-" * 5,
            name="-" * 15,
            tagged_items="-" * 12,
            rgb="-" * 6,
            color="-" * 10,
            description="-" * 30,
        )
    )


def print_values():
    """
    print column values (tag info)
    """
    tags = nb.extras.tags.all()
    for tag in tags:
        print(
            get_fmt().format(
                id=tag.id,
                name=tag.name,
                tagged_items=tag.tagged_items,
                rgb=tag.color,
                color=color(tag.color),
                description=tag.description,
            )
        )


cfg = get_parser()
nb = netbox()
print_headers()
print_values()
