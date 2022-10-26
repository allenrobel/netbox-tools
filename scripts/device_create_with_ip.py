#!/usr/bin/env python3
'''
Name: device_create_with_ip.py
Summary: Create a device in netbox
See also: device_create_all.py

This script does the following:
  1. Create, or update, device
  2. Create mgmt0 interface for device
  3. Add IPv4 address to mgmt0 interface
  4. Make IPv4 address the primary_ip for device

Example usage:

./device_create_2.py \
        --device foo \
        --interface mgmt0 \
        --mgmt_ip 10.10.10.10/24 \
        --role lab_tor \
        --site SJC03-1-155 \
        --serial CN943G \
        --tags admin,lab_infra \
        --type CISCO-2600
'''

our_version = 100
from lib.common import ip_address_id, interface_id
from lib.device import Device, initialize_device_primary_ip, map_device_primary_ip, make_device_primary_ip
from lib.interface import Interface
from lib.ip_address import IpAddress
import pynetbox
import argparse

from lib.credentials import NetboxCredentials
from lib.common import get_device

help_device = 'Name of the device to add.'
help_interface = 'Management interface for the device.'
help_mgmt_ip = 'Management IPv4 address for the device.'
help_role = 'Role for the device. Role must already exist in netbox.'
help_serial = 'Optional. Default: na. Serial number of the device.'
help_site = 'Site in which device will reside. Site must already exist in netbox.'
help_tags = 'Optional. Comma-separated list of pre-existing tags to associate with the device. All tags must already exist in netbox.'
help_type = 'Type of device (i.e. model number). model number must already exist in netbox'
ex_prefix     = 'Example: '
ex_device = '{} --device leaf_3'.format(ex_prefix)
ex_interface = '{} --interface mgmt0'.format(ex_prefix)
ex_mgmt_ip = '{} --mgmt_ip 192.168.1.5/24'.format(ex_prefix)
ex_role = '{} --role leaf'.format(ex_prefix)
ex_serial = '{} --serial CX045BN'.format(ex_prefix)
ex_site = '{} --site f1'.format(ex_prefix)
ex_tags = '{} --tags poc,admin'.format(ex_prefix)
ex_type = '{} --type N9K-C93180YC-EX'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Add a device')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--device',
                     dest='device',
                     required=True,
                     help=help_device + ex_device)
mandatory.add_argument('--interface',
                     dest='interface',
                     required=True,
                     help=help_interface + ex_interface)
mandatory.add_argument('--mgmt_ip',
                     dest='mgmt_ip',
                     required=True,
                     help=help_mgmt_ip + ex_mgmt_ip)
mandatory.add_argument('--role',
                     dest='role',
                     required=True,
                     help=help_role + ex_role)
default.add_argument('--serial',
                     dest='serial',
                     required=False,
                     default=None,
                     help=help_serial + ex_serial)
mandatory.add_argument('--site',
                     dest='site',
                     required=True,
                     help=help_site + ex_site)
default.add_argument('--tags',
                     dest='tags',
                     required=False,
                     default=None,
                     help=help_tags + ex_tags)
mandatory.add_argument('--type',
                     dest='type',
                     required=True,
                     help=help_type + ex_type)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_tags():
    tags = list()
    for tag in cfg.tags.split(','):
        tags.append(tag)
    return tags
def get_info():
    info = dict()
    info['mgmt_ip'] = cfg.mgmt_ip
    info['interface'] = cfg.interface
    info['device'] = cfg.device
    info['role'] = cfg.role
    if cfg.serial != None:
        info['serial'] = cfg.serial
    else:
        cfg.serial = 'na'
    info['site'] = cfg.site
    if cfg.tags != None:
        info['tags'] = get_tags()
    info['type'] = cfg.type
    return info

def assign_primary_ip_to_device(info):
    ipv4_id = ip_address_id(nb, info['mgmt_ip'])
    intf_id = interface_id(nb, info['device'], info['interface'])
    if ipv4_id == None:
        print('assign_primary_ip_to_device: Exiting. Address {} not found in netbox'.format(info['mgmt_ip']))
        exit(1)
    if intf_id == None:
        print('assign_primary_ip_to_device: Exiting. Interface {} not found in netbox'.format(info['interface']))
        exit(1)
    initialize_device_primary_ip(nb, info['device'])
    map_device_primary_ip(nb, info['device'], info['interface'], info['mgmt_ip'])
    make_device_primary_ip(nb, info['device'], info['mgmt_ip'])

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)

info = get_info()
print('---')
d = Device(nb, info)
d.create_or_update()
i = Interface(nb, info)
i.create_or_update()
ip = IpAddress(nb, info)
ip.create_or_update()
assign_primary_ip_to_device(info)