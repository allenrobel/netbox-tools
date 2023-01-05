#!/usr/bin/env python3
'''
Name: tags_print.py
Description: Display information about all tags
'''
OUR_VERSION = 103
import argparse

from netbox_tools.colors import color
from netbox_tools.common import netbox

def get_parser():
    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Display information about all tags')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(OUR_VERSION))

    return parser.parse_args()

def get_fmt():
    return '{:>5} {:<15} {:>12} {:>6} {:<10} {:<30}'

def print_headers():
    fmt = get_fmt()
    print(fmt.format('id', 'name', 'tagged_items', 'rgb', 'color', 'description'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 12, '-' * 6, '-' * 10, '-' * 30))

def print_tags():
    tags = nb.extras.tags.all()
    fmt = get_fmt()
    for tag in tags:
        print(fmt.format(tag.id, tag.name, tag.tagged_items, tag.color, color(tag.color), tag.description))

cfg = get_parser()
nb = netbox()

print_headers()
print_tags()
