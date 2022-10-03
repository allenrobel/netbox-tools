#!/usr/bin/env python3
'''
Name: rack_create_update.py
Description: Create or update a Netbox rack.
Example Usage:

./rack_create_update.py --rack A001 --location row-a --site volcano --u_height 48 --comments "a comment" --tags infra,admin
'''
our_version = 100
import argparse
from lib.common import netbox, load_yaml
from lib.rack import Rack
import re

help_location = 'Location of --rack'
help_comments = 'Free-form comment for --rack'
help_rack = 'Rack name'
help_site = 'Site containing --rack'
help_tags = 'Comma-separated list of tags (no spaces) to apply to this rack. All tags must already exist in Netbox.'
help_u_height = 'Height of --rack in RU (rack units)'

ex_prefix     = 'Example: '
ex_comments = '{} --comments "this is a rack comment"'.format(ex_prefix)
ex_location = '{} --location row-c'.format(ex_prefix)
ex_rack = '{} --rack C004'.format(ex_prefix)
ex_site = '{} --site mysite'.format(ex_prefix)
ex_tags = '{} --tags admin,infra'.format(ex_prefix)
ex_u_height = '{} --u_height 48'.format(ex_prefix)
parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update a Netbox rack')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
optional   = parser.add_argument_group(title='OPTIONAL SCRIPT ARGS')

optional.add_argument('--comments',
                     dest='comments',
                     required=False,
                     default=None,
                     help=help_comments + ex_comments)
mandatory.add_argument('--location',
                     dest='location',
                     required=True,
                     help=help_location + ex_location)
mandatory.add_argument('--rack',
                     dest='rack',
                     required=True,
                     help=help_rack + ex_rack)
mandatory.add_argument('--site',
                     dest='site',
                     required=True,
                     help=help_site + ex_site)
optional.add_argument('--tags',
                     dest='tags',
                     required=False,
                     default=None,
                     help=help_tags + ex_tags)
optional.add_argument('--u_height',
                     dest='u_height',
                     required=False,
                     default=None,
                     help=help_u_height + ex_u_height)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.rack
    info['location'] = cfg.location
    info['site'] = cfg.site
    if cfg.comments != None:
        info['comments'] = cfg.comments
    if cfg.u_height != None:
        info['u_height'] = cfg.u_height
    if cfg.tags != None:
        info['tags'] = re.split(',', cfg.tags)
    return info

nb = netbox()
info = get_info()
rack = Rack(nb, info)
rack.create_or_update()

