#!/usr/bin/env python3
'''
Name: location_delete.py
Description: Delete location ``--location`` from netbox
'''
OUR_VERSION = 102
import argparse

from netbox_tools.common import netbox
from netbox_tools.location import Location

def get_parser():
    help_location = 'Name of the location to delete.'

    ex_prefix = ' Example: '
    ex_location = '{} --location mylocation'.format(ex_prefix)

    parser = argparse.ArgumentParser(description='DESCRIPTION: Delete location --location from netbox')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--location',
                        dest='location',
                        required=True,
                        help=help_location + ex_location)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(OUR_VERSION))

    return parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.location
    return info

cfg = get_parser()
nb = netbox()
l = Location(nb, get_info())
l.delete()
