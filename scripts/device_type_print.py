#!/usr/bin/env python3
'''
Name: device_type_print.py
Description: Display information about a device type
'''
our_version = 101
import argparse
import json
from lib.common import netbox

help_detail = 'Optional. If present, print detailed info about the device_type (aka model).'
help_model = 'Retrieve and display information for model.'

ex_prefix = ' Example: '
ex_detail = '{} --detail'.format(ex_prefix)
ex_model = '{} --model N9K-C93180YC-EX'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Print information for a device model (Netbox device model is roughly equivilent to model number)')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--model',
                     dest='model',
                     required=True,
                     help=help_model + ex_model)

default.add_argument('--detail',
                     dest='detail',
                     required=False,
                     default=False,
                     action='store_true',
                     help=help_detail + ex_detail)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()


def error():
    device_types = list()
    items = nb.dcim.device_types.all()
    for item in items:
        device_types.append(item.model)
    print('Device type (aka model) {} does not exist in netbox.  Valid device types: {}'.format(cfg.model, ', '.join(device_types)))
    exit(1)
def get_device_type():
    device_type = nb.dcim.device_types.get(model=cfg.model)
    if device_type == None:
        error()
    return device_type

def print_detail(device_type):
    pretty = json.dumps(dict(device_type), indent=4, sort_keys=True)
    print(pretty)

def print_headers():
    print(fmt.format('id', 'model', 'device_count', 'manufacturer'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 12, '-' * 20))

nb = netbox()

device_type = get_device_type()
if cfg.detail:
    print_detail(device_type)
else:
    fmt = '{:>5} {:<15} {:>12} {:<20}'
    print_headers()
    print(fmt.format(device_type.id, device_type.model, device_type.device_count, device_type.manufacturer.name))
