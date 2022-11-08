#!/usr/bin/env python3
'''
Name: console_ports_print.py
Description: Display information about all console_ports
'''
our_version = 100
import argparse
from netbox_tools.common import netbox, get_console_ports

def get_parser():
    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Display information about all console_ports')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

def print_headers():
    print(fmt.format('id',    'device', 'port',   'tags',   'description'))
    print(fmt.format('-' * 4, '-' * 15, '-' * 15, '-' * 15, '-'* 15))
def get_tag_names(tags_list):
    tag_names = list()
    for tag_record in tags_list:
        tag_dict = dict(tag_record)
        tag_names.append(tag_dict['name'])
    return tag_names
        
fmt = '{:>4} {:<15} {:<15} {:<15} {:<15}'

cfg = get_parser()
nb = netbox()

console_ports = get_console_ports(nb)
print_headers()
for console_port in console_ports:
    print(fmt.format(
        console_port.id,
        console_port.device.name,
        console_port.name,
        ','.join(get_tag_names(console_port.tags)),
        console_port.description))
