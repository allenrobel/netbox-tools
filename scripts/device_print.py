#!/usr/bin/env python3
'''
Name: device_print.py
Description: Print information about a device
'''
our_version = 102
import argparse
import json
from netbox_tools.common import netbox

def get_parser():
    help_name = 'Name of device to retrieve.'
    help_detail = 'Optional. If present, print detailed info about device.'

    ex_prefix     = 'Example: '
    ex_name = '{} --name leaf_3'.format(ex_prefix)
    ex_detail = '{} --detail'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Print information about a device')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--name',
                        dest='name',
                        required=True,
                        help=help_name + ex_name)
    default.add_argument('--detail',
                        dest='detail',
                        required=False,
                        default=False,
                        action='store_true',
                        help=help_detail + ex_detail)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()


def get_device():
    device = nb.dcim.devices.get(name=cfg.name)
    if device == None:
        print('Device {} does not exist in netbox.'.format(cfg.name))
        exit(1)
    return device

def print_detail():
    pretty = json.dumps(dict(device), indent=4, sort_keys=True)
    print(pretty)

def print_headers():
    print(fmt.format('id', 'device_name', 'comments'))
    print(fmt.format('-' * 5, '-' * 20, '-' * 30))

fmt = '{:>5} {:<20} {:<30}'

cfg = get_parser()
nb = netbox()
device = get_device()
if cfg.detail:
    print_detail()
else:
    print_headers()
    print(fmt.format(device.id, device.name, device.comments))
