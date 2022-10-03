#!/usr/bin/env python3
'''
Name: device_print_filtered.py
Summary: Print devices filtered by tags and/or model
Description:

If the --tags or --model arguments are not provided, print information for all devices.
If the --tags argument is provided, print information for devices that match the boolean ANDed set of tags.
If the --model argument is provided, print information for devices that match model number.
If both --tags and --model arguments are provided, print information for devices that match model AND boolean ANDed set of tags.

For example:

   --tags foo,bar,baz --model N9K-C9336C-FX2

Would match N9K-C9336C-FX2 that contain all three tags foo, bar, and baz.
'''
import argparse
import pynetbox
from lib.common import netbox

our_version = 100

help_tags = 'Comma-separated list of tags (no spaces). If present, only devices containing tag(s) are printed.  Else, all devices are printed.'
help_model = 'Device model number'

ex_prefix     = ' Example: '
ex_tags = '{} --tags deathstar,admin'.format(ex_prefix)
ex_model = '{} --model N9K-C9336C-FX2'

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Print list of devices filtered by tag and/or model')

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
        'tags'))
    print(fmt.format(
        '-' * 9,
        '-' * 18,
        '-' * 18,
        '-' * 12,
        '-' * 22,
        '-' * 6,
        '-' * 10,
        '-' * 15))

def get_primary_ip(device):
    if device.primary_ip4 == None:
        return 'na'
    else:
        return str(device.primary_ip4)

def get_primary_ip_id(device):
    if device.primary_ip4 == None:
        return 'na'
    else:
        return device.primary_ip4.id

def get_tags(device):
    tags = device.tags
    if tags == None:
        return ""
    return ','.join([tag.name for tag in device.tags])

def print_matches(matches):
    print_header()
    for device_name in matches:
        if matches[device_name] == False:
            continue
        device = matches[device_name]
        print(fmt.format(
            device.id,
            device.name,
            device.device_type.model,
            device.serial,
            get_primary_ip(device),
            get_primary_ip_id(device),
            str(device.status),
            get_tags(device)))

def unfiltered(devices):
    matches = dict()
    for device in devices:
        matches[device.name] = device
    return matches
def filtered_on_tag(matches):
    user_tags = set(cfg.tags.split(','))
    for device in matches:
        if matches[device] == False:
            continue
        device_tag_objects = matches[device].tags
        device_tags = set()
        for device_tag_object in device_tag_objects:
            device_tags.add(device_tag_object.name)
        if user_tags.issubset(device_tags):
            continue
        matches[device] = False
    return matches
def filtered_on_model(matches):
    for device in matches:
        if matches[device] == False:
            continue
        if matches[device].device_type.model != cfg.model:
            matches[device] = False
    return matches


fmt = '{:<9} {:<18} {:<18} {:<12} {:<22} {:<6} {:<10} {:<15}'

nb = netbox()
devices = nb.dcim.devices.all()

matches = unfiltered(devices)
if cfg.tags != None:
    matches = filtered_on_tag(matches)
if cfg.model != None:
    matches = filtered_on_model(matches)

print_matches(matches)