#!/usr/bin/env python3
'''
Name: site_delete.py
Description: Delete site ``--site``
'''
OUR_VERSION = 103
import argparse

from netbox_tools.common import netbox
from netbox_tools.site import Site

def get_parser():
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
                        version='%(prog)s {}'.format(OUR_VERSION))

    return parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.site
    return info

cfg = get_parser()
nb = netbox()
d = Site(nb, get_info())
d.delete()
