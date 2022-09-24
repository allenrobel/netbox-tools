#!/usr/bin/env python3
'''
Name: device_types_print.py
Description: Print information about all device types
'''
our_version = 100
import argparse
import json
import pynetbox
from lib.credentials import NetboxCredentials

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Print information about all device types')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_device_types():
    try:
        device_types = nb.dcim.device_types.all()
        return device_types
    except Exception as e:
        print('Could not retrieve device types. Error was {}'.format(e))

def print_detail(device_type):
    pretty = json.dumps(dict(device_type), indent=4, sort_keys=True)
    print(pretty)

def print_headers():
    print(fmt.format('id', 'name', 'device_count', 'manufacturer'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 12, '-' * 20))

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)

device_types = get_device_types()
fmt = '{:>5} {:<15} {:>12} {:<20}'
print_headers()
for dt in device_types:
    print(fmt.format(dt.id, dt.model, dt.device_count, dt.manufacturer.name))
