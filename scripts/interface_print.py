#!/usr/bin/env python3
'''
Name: interface_print.py
Description: Display interface information for ``--device`` ``--interface``
'''
our_version = 100
import argparse
import json
from lib.common import netbox

help_detail = 'Optional. If present, print detailed info about device.'
help_device = 'Name of the device on which interface resides.'
help_interface = 'Name of the interface.'

ex_prefix     = 'Example: '
ex_detail = '{} --detail'.format(ex_prefix)
ex_device = '{} --device leaf_3'.format(ex_prefix)
ex_interface = '{} --interface mgmt0'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Print information about an interfaces')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

default.add_argument('--detail',
                     dest='detail',
                     required=False,
                     default=False,
                     action='store_true',
                     help=help_detail + ex_detail)
mandatory.add_argument('--device',
                     dest='device',
                     required=True,
                     help=help_device + ex_device)
mandatory.add_argument('--interface',
                     dest='interface',
                     required=True,
                     help=help_interface + ex_interface)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_interface():
    interface = nb.dcim.interfaces.get(device=cfg.device, name=cfg.interface)
    if interface == None:
        print('Device {} interface {} does not exist in netbox.'.format(cfg.device, cfg.interface))
        exit(1)
    return interface

def print_detail(interface):
    pretty = json.dumps(dict(interface), indent=4, sort_keys=True)
    print(pretty)

def print_headers():
    print(fmt.format(   'id', 'device_name', 'interface', 'mac_address',       'type',    'enabled', 'mgmt_only'))
    print(fmt.format('-' * 5,      '-' * 20,    '-' * 15,     '-' * 17,      '-' * 15,      '-' * 7,     '-' * 9))

fmt = '{:>5} {:<20} {:<15} {:<17} {:<15} {:<7} {:<9}'

nb = netbox()

interface = get_interface()
if cfg.detail:
    print_detail(interface)
else:
    print_headers()
    print(fmt.format(interface.id, interface.device.name, interface.name, str(interface.mac_address), interface.type.value, str(interface.enabled), str(interface.mgmt_only)))
