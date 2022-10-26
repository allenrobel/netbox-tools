#!/usr/bin/env python3
'''
Name: console_server_ports_print.py
Description: Display information about all console_server_ports
'''
our_version = 100
import argparse
from lib.common import netbox, get_console_server_ports


parser = argparse.ArgumentParser(
         description='DESCRIPTION: Display information about all console_server_ports')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def print_headers():
    print(fmt.format('id',    'device', 'port',   'tags',   'description'))
    print(fmt.format('-' * 4, '-' * 15, '-' * 15, '-' * 15, '-'* 15))

fmt = '{:>4} {:<15} {:<15} {:<15} {:<15}'

nb = netbox()

console_server_ports = get_console_server_ports(nb)
print_headers()
for console_server_port in console_server_ports:
    print(fmt.format(
        console_server_port.id,
        console_server_port.device.name,
        console_server_port.name,
        ','.join(console_server_port.tags),
        console_server_port.description))
