#!/usr/bin/env python3
'''
Name: interfaces_print.py
Description: Print information about all interfaces
'''
import argparse

from lib.common import netbox

def get_fmt():
    return '{:>5} {:<20} {:<15} {:<17} {:<12} {:<7} {:<9}'

def print_headers():
    fmt = get_fmt()
    print(fmt.format(   'id', 'device_name', 'interface', 'mac_address',       'type',    'enabled', 'mgmt_only'))
    print(fmt.format('-' * 5,      '-' * 20,    '-' * 15,     '-' * 17,      '-' * 12,      '-' * 7,     '-' * 9))

def print_items(items):
    fmt = get_fmt()
    for item in items:
        print(fmt.format(item.id, item.device.name, item.name, str(item.mac_address), item.type.value, item.enabled, item.mgmt_only))

def get_interfaces():
    i = nb.dcim.interfaces.all()
    if i == None:
        print('Exiting: no interfaces')
        exit(1)
    return i

nb = netbox()

response = get_interfaces()
print_headers()
print_items(response)
