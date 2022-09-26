#!/usr/bin/env python3
'''
Name: site_delete.py
Description: Delete site --site from netbox
'''
our_version = 100
import argparse
import pynetbox

from lib.credentials import NetboxCredentials
from lib.site import Site

help_site = 'Name of the site to delete.'

ex_prefix = ' Example: '
ex_site = '{} --site mysite'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a site')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--site',
                     dest='site',
                     required=True,
                     help=help_site + ex_site)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.site
    return info

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)
d = Site(nb, get_info())
d.delete()
