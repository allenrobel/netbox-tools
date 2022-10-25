#!/usr/bin/env python3
'''
Name: entity_create_all.py
Summary: Create/update all Netbox entities (console server ports, device types, etc) from information in a YAML file.
Description:

This script does the following, using the YAML contained in --yaml

See ./info.yml for the YAML structure this script assumes.

1.  Create, or update, sites
2.  Create, or update, locations
3.  Create, or update, manufacturers
4.  Create, or update, device_types
5.  Create, or update, device_roles
6.  Create, or update, racks
7.  Create, or update, tags
8.  Create, or update, devices
    8a. Create management interface for device
    8b. Add IPv4 address to the management interface
    8c. Make IPv4 address the primary_ip for device

'''
our_version = 101

import argparse
# Local libraries
from lib.common import netbox, device_id, get_device, interface_id, ip_address_id, get_ip_address, location_id, get_manufacturer, rack_id
from lib.common import load_yaml
from lib.console_server_port import ConsoleServerPort
from lib.device import Device, initialize_device_primary_ip, make_device_primary_ip, map_device_primary_ip
from lib.device_type import DeviceType
from lib.interface import Interface
from lib.ip_address import IpAddress
from lib.ip_prefix import IpPrefix
from lib.location import Location
from lib.manufacturer import Manufacturer
from lib.rack import Rack
from lib.role import Role
from lib.site import Site
from lib.tag import Tag

from lib.credentials import NetboxCredentials

help_yaml = 'JSON file to open (contains testbed info)'

ex_prefix     = 'Example: '
ex_yaml = '{} --yaml /my/yaml/file.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Delete a device')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--yaml',
                     dest='yaml',
                     required=True,
                     help=help_yaml + ex_yaml)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

# Used for backward-compatibility. Remove after 2022-09-29
def fix_deprecations():
    if 'mgmt_interface' in info:
        print('device_create_update_all.fix_deprecations: WARNING: devices: <device>: mgmt_interface in your YAML file is deprecated. Use devices: <device>: interface instead.')
        info['interface'] = info['mgmt_interface']
    if 'name' in info:
        print('device_create_update_all.fix_deprecations: WARNING: devices: <device>: name in your YAML file is deprecated. Use devices: <device>: device instead.')
        info['device'] = info['name']

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

nb = netbox()

info = load_yaml(cfg.yaml)
fix_deprecations()
print('---')
for key in info['console_server_ports']:
    c = ConsoleServerPort(nb, info['console_server_ports'][key])
    c.create_or_update()
for key in info['tags']:
    t = Tag(nb, info['tags'][key])
    t.create_or_update()
for key in info['sites']:
    s = Site(nb, info['sites'][key])
    s.create_or_update()
print('---')
for key in info['locations']:
    l = Location(nb, info['locations'][key])
    l.create_or_update()
print('---')
for key in info['manufacturers']:
    m = Manufacturer(nb, info['manufacturers'][key])
    m.create_or_update()
print('---')
for key in info['device_types']:
    m = DeviceType(nb, info['device_types'][key])
    m.create_or_update()
print('---')
for key in info['device_roles']:
    r = Role(nb, info['device_roles'][key])
    r.create_or_update()
print('---')
for key in info['racks']:
    r = Rack(nb, info['racks'][key])
    r.create_or_update()
print('---')
for key in info['prefixes']:
    p = IpPrefix(nb, info['prefixes'][key])
    p.create_or_update()
for key in info['devices']:
    print('---')
    d = Device(nb, info['devices'][key])
    d.create_or_update()
    i = Interface(nb, info['devices'][key])
    i.create_or_update()
    ip = IpAddress(nb, info['devices'][key])
    ip.create_or_update()
    assign_primary_ip_to_device(info['devices'][key])