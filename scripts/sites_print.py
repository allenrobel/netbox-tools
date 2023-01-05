#!/usr/bin/env python3
'''
Name: sites_print.py
Description: Display information about all sites
'''
OUR_VERSION = 103
import argparse
from netbox_tools.common import netbox

def get_parser():
    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Display information about all sites')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(OUR_VERSION))

    return parser.parse_args()

def get_fmt():
    return '{:>5} {:<15} {:>12} {:>12} {:>12} {:<10} {:<30}'
    
def print_headers():
    fmt = get_fmt()
    print(fmt.format('id', 'name', 'device_count', 'rack_count', 'prefix_count', 'status', 'description'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 12, '-' * 12, '-' * 12, '-' * 10, '-' * 30))

def print_sites():
    sites = nb.dcim.sites.all()
    if sites == None:
        exit()
    fmt = get_fmt()
    for site in sites:
        print(fmt.format(site.id, site.name, site.device_count, site.rack_count, site.prefix_count, site.status.value, site.description))

cfg = get_parser()
nb = netbox()
print_headers()
print_sites()
