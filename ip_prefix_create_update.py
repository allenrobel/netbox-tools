#!/usr/bin/env python3
'''
Name: ip_prefix_create.py
Description: Create an ip prefix in netbox
'''
our_version = 100
import pynetbox
import argparse

from lib.credentials import NetboxCredentials
from lib.ip_prefix import IpPrefix

help_description = 'Optional. Quoted free-form description for this prefix'
help_prefix = 'Prefix to create'
help_site = 'Optional. Site in which prefix will be used'
help_status = 'Optional. Status of the ip prefix (container, active, reserved, deprecated)'

_ex_prefix_ = ' Example: '
ex_description = '{} --description "this is a description"'.format(_ex_prefix_)
ex_prefix = '{} --prefix 192.168.1.0/24'.format(_ex_prefix_)
ex_site = '{} --site SJC03-1-155'.format(_ex_prefix_)
ex_status = '{} --status active'.format(_ex_prefix_)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Add a prefix')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
optional   = parser.add_argument_group(title='OPTIONAL SCRIPT ARGS')

optional.add_argument('--description',
                     dest='description',
                     required=False,
                     default=None,
                     help=help_description + ex_description)

optional.add_argument('--site',
                     dest='site',
                     required=False,
                     default=None,
                     help=help_site + ex_site)

mandatory.add_argument('--prefix',
                     dest='prefix',
                     required=True,
                     help=help_prefix + ex_prefix)

optional.add_argument('--status',
                     dest='status',
                     required=False,
                     default=None,
                     help=help_status + ex_status)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)

info = dict()
info['prefix'] = cfg.prefix
if cfg.description != None:
    info['description'] = cfg.description
if cfg.status != None:
    info['status'] = cfg.status
if cfg.site != None:
    info['site'] = cfg.site

p = IpPrefix(nb, info)
p.create_or_update()
