#!/usr/bin/env python3
'''
Name: racks_print.py
Description: Display information about all racks
'''
OUR_VERSION = 103
import argparse
from netbox_tools.common import netbox

def get_parser():
    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Display information about all racks')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(OUR_VERSION))

    return parser.parse_args()

def get_racks():
    return nb.dcim.racks.all()

def print_headers():
    print(fmt.format('id', 'name', 'site'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 15))


cfg = get_parser()
nb = netbox()
racks = get_racks()

fmt = '{:>5} {:>15} {:>15}'

print_headers()
for rack in racks:
    print(fmt.format(rack.id, rack.name, rack.site.name))
