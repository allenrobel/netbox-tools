#!/usr/bin/env python3
'''
Name: tags_print.py
Description: Print information about all tags
'''
our_version = 101
import argparse

from lib.colors import color
from lib.common import netbox

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Print information about all tags')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

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

nb = netbox()

print_headers()
print_tags()
