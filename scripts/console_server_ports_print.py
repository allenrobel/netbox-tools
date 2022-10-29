#!/usr/bin/env python3
'''
Name: console_server_ports_print.py
Description: Display information about all console_server_ports
'''
our_version = 101
import argparse
from netbox_tools.common import netbox, get_console_server_ports


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
def get_tag_names(tags_list):
    tag_names = list()
    for tag_record in tags_list:
        tag_dict = dict(tag_record)
        tag_names.append(tag_dict['name'])
    return tag_names
        
fmt = '{:>4} {:<15} {:<15} {:<15} {:<15}'

nb = netbox()

console_server_ports = get_console_server_ports(nb)
print_headers()
for console_server_port in console_server_ports:
    #print('port {}'.format(dict(console_server_port)))
    print(fmt.format(
        console_server_port.id,
        console_server_port.device.name,
        console_server_port.name,
        ','.join(get_tag_names(console_server_port.tags)),
        console_server_port.description))
