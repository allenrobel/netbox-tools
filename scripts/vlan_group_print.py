#!/usr/bin/env python3
'''
Name: vlan_group_print.py
Description: Display information about vlan_group ``--vlan_group``
'''
OUR_VERSION = 103
import argparse
import json
from netbox_tools.common import netbox

def get_parser():
    help_detail = 'Optional. If present, print detailed info about VlanGroup.'
    help_vlan_group = 'Name of the VlanGroup.'

    ex_prefix     = 'Example: '
    ex_detail = '{} --detail'.format(ex_prefix)
    ex_vlan_group = '{} --vlan_group AdminServers'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Display information about a VlanGroup')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    default.add_argument('--detail',
                        dest='detail',
                        required=False,
                        default=False,
                        action='store_true',
                        help=help_detail + ex_detail)
    mandatory.add_argument('--vlan_group',
                        dest='vlan_group',
                        required=True,
                        help=help_vlan_group + ex_vlan_group)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(OUR_VERSION))

    return parser.parse_args()

def error():
    vlan_groups = list()
    items = nb.ipam.vlan_groups.all()
    for item in items:
        vlan_groups.append(item.name)
    print('vlan_group {} does not exist in netbox.  Valid vlan_groups: {}'.format(cfg.vlan_group, ', '.join(vlan_groups)))
    exit(1)

def get_vlan_group():
    vlan_group = nb.ipam.vlan_groups.get(name=cfg.vlan_group)
    if vlan_group == None:
        error()
    return vlan_group

def print_detail():
    pretty = json.dumps(dict(vlan_group), indent=4, sort_keys=True)
    print(pretty)

def print_headers():
    print(fmt.format('id',    'name',   'min_vid', 'max_vid', 'description'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 7,    '-' * 7,   '-' * 25))


cfg = get_parser()
nb = netbox()
vlan_group = get_vlan_group()

fmt = '{:>5} {:>15} {:>7} {:>7} {:>25}'

if cfg.detail:
    print_detail()
    exit()

print_headers()
print(fmt.format(vlan_group.id, vlan_group.name, vlan_group.min_vid, vlan_group.max_vid, str(vlan_group.description)))
