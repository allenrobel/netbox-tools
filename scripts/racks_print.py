#!/usr/bin/env python3
'''
Name: racks_print.py
Description: Display information about all racks
'''
our_version = 102
import argparse
from netbox_tools.common import netbox


parser = argparse.ArgumentParser(
         description='DESCRIPTION: Display information about all racks')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_racks():
    return nb.dcim.racks.all()

def print_headers():
    print(fmt.format('id', 'name', 'site'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 15))

fmt = '{:>5} {:>15} {:>15}'

nb = netbox()

racks = get_racks()
print_headers()
for rack in racks:
    print(fmt.format(rack.id, rack.name, rack.site.name))
