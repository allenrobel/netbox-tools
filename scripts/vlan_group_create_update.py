#!/usr/bin/env python3
'''
Name: vlan_group_create_update.py
Description: Create/update a vlan_group with command line options ``--description``, ``--max_vid``, ``--min_vid``, ``--tags``, ``--vlan_group``
Example Usage:

./vlan_group_create_update.py --vlan_group AdminServers --min_vid 1 --max_vid 15 --description "Admin Server Vlans" --tags server,admin

'''
OUR_VERSION = 102
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.vlan_group import VlanGroup
import re

def get_parser():
    help_description = 'Optional. Free-form description for this VlanGroup. '
    help_max_vid = 'Optional. Maximum vlan id for this VlanGroup. Default: 1 '
    help_min_vid = 'Optional. Minimum vlan id for this VlanGroup. Default: 4094 '
    help_tags = 'Optional. Comma-separated list of tags (no spaces) to apply to this VlanGroup. All tags must already exist in Netbox. '
    help_vlan_group = 'Name of this VlanGroup'

    ex_prefix     = 'Example: '
    ex_description = '{} --description "this is a vlan_group description"'.format(ex_prefix)
    ex_max_vid = '{} --max_vid 10'.format(ex_prefix)
    ex_min_vid = '{} --min_vid 2'.format(ex_prefix)
    ex_tags = '{} --tags admin,infra'.format(ex_prefix)
    ex_vlan_group = '{} --vlan_group AdminServers'.format(ex_prefix)
    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create/update a vlan_group with command line options')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    optional   = parser.add_argument_group(title='OPTIONAL SCRIPT ARGS')

    optional.add_argument('--max_vid',
                        dest='max_vid',
                        required=False,
                        default=None,
                        help=help_max_vid + ex_max_vid)
    optional.add_argument('--min_vid',
                        dest='min_vid',
                        required=False,
                        default=None,
                        help=help_min_vid + ex_min_vid)
    optional.add_argument('--description',
                        dest='description',
                        required=False,
                        default=None,
                        help=help_description + ex_description)
    mandatory.add_argument('--vlan_group',
                        dest='vlan_group',
                        required=True,
                        help=help_vlan_group + ex_vlan_group)
    mandatory.add_argument('--tags',
                        dest='tags',
                        required=False,
                        default=None,
                        help=help_tags + ex_tags)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(OUR_VERSION))

    return parser.parse_args()

def get_info():
    info = dict()
    info['vlan_group'] = cfg.vlan_group
    if cfg.description != None:
        info['description'] = cfg.description
    if cfg.min_vid != None:
        info['min_vid'] = cfg.min_vid
    if cfg.max_vid != None:
        info['max_vid'] = cfg.max_vid
    if cfg.tags != None:
        info['tags'] = re.split(',', cfg.tags)
    return info

cfg = get_parser()
nb = netbox()
info = get_info()
vlan_group = VlanGroup(nb, info)
vlan_group.create_or_update()
