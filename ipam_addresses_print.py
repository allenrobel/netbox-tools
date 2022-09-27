#!/usr/bin/env python3
'''
Name: ipam_addresses_print.py
Description: Print all ip addresses
'''
from lib.common import netbox

def get_fmt():
    return '{:>5} {:<18} {:<18} {:<30}'

def print_ip_addresses():
    items = nb.ipam.ip_addresses.all()
    if items == None:
        exit()
    fmt = get_fmt()
    for item in items:
        if item.assigned_object == None:
            print(fmt.format(item.id, item.address, 'na', item.description))
        else:
            print(fmt.format(item.id, item.address, item.assigned_object.device.name, item.description))

def print_headers():
    fmt = get_fmt()
    print(fmt.format('id', 'address', 'device_name', 'description'))
    print(fmt.format('-' * 5, '-' * 18, '-' * 18, '-' * 30))

nb = netbox()

print_headers()
print_ip_addresses()