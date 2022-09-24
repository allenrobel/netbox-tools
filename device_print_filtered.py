#!/usr/bin/env python3
'''
Name: device_print_filtered.py
Summary: Print devices filtered by tags or model
Description:

If the --tags or --model arguments are not provided, print information for all devices
If the --tags argument is provided, print information for devices that match the boolean ANDed set of tags.
If the --model argument is provided, print information for devices that match model number.

For example:

   --tags foo,bar,baz

Would match devices that contain all three tags foo, bar, and baz.

Or:

   --model N9K-C9336C-FX2

Would match devices with model number N9K-C9336C-FX2

--tags and --model are mutually-exclusive
'''
import argparse
import pynetbox
from lib.credentials import NetboxCredentials

our_version = 100

help_tags = 'Comma-separated list of tags (no spaces). If present, only devices containing tag(s) are printed.  Else, all devices are printed.'
help_model = 'Device model number'

ex_prefix     = ' Example: '
ex_tags = '{} --tags arobel,cvd_poc'.format(ex_prefix)
ex_model = '{} --model N9K-C9336C-FX2'

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Filter devices by tag')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

default.add_argument('--tags',
                     dest='tags',
                     required=False,
                     help=help_tags + ex_tags)
default.add_argument('--model',
                     dest='model',
                     required=False,
                     help=help_model + ex_model)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def print_header():
    print(fmt.format(
        'device_id',
        'name',
        'model',
        'serial',
        'primary_ip4',
        'ip4_id',
        'status',
    ))
    print(fmt.format(
        '-' * 9,
        '-' * 18,
        '-' * 18,
        '-' * 12,
        '-' * 22,
        '-' * 6,
        '-' * 10,
    ))

def print_filtered_model(devices):
    matches = dict()
    for device in devices:
        matches[device.name] = device
        if device.device_type.model != cfg.model:
            matches[device.name] = False
    for device_name in matches:
        if matches[device_name] == False:
            continue
        device = matches[device_name]
        if device.primary_ip4 == None:
            print(fmt.format(device.id, device.name, device.device_type.model, device.serial, 'na', 'na', str(device.status)))
        else:
            print(fmt.format(device.id, device.name, device.device_type.model, device.serial, str(device.primary_ip4.address), device.primary_ip4.id, str(device.status)))

def print_filtered_tag(devices):
    tags = cfg.tags.split(',')
    matches = dict()
    for device in devices:
        matches[device.name] = device
        for tag in tags:
            if tag not in [tag.name for tag in device.tags]:
                matches[device.name] = False
    for device_name in matches:
        if matches[device_name] == False:
            continue
        device = matches[device_name]
        if device.primary_ip4 == None:
            print(fmt.format(device.id, device.name, device.device_type.model, device.serial, 'na', 'na', str(device.status)))
        else:
            print(fmt.format(device.id, device.name, device.device_type.model, device.serial, str(device.primary_ip4.address), device.primary_ip4.id, str(device.status)))

def print_devices(devices):
    for device in devices:
        if device.primary_ip4 == None:
            print(fmt.format(device.id, device.name, device.device_type.model, device.serial, 'na', 'na', str(device.status)))
        else:
            print(fmt.format(device.id, device.name, device.device_type.model, device.serial, str(device.primary_ip4.address), device.primary_ip4.id, str(device.status)))


fmt = '{:<9} {:<18} {:<18} {:<12} {:<22} {:<6} {:<10}'

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)
devices = nb.dcim.devices.all()

if cfg.tags != None and cfg.model != None:
    print('exiting. --tags and --model are mutually-exclusive. Use one or the other, but not both.')
    exit(1)
print_header()
if cfg.tags != None:
    print_filtered_tag(devices)
elif cfg.model != None:
    print_filtered_model(devices)
else:
    print_devices(devices)
