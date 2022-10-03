#!/usr/bin/env python3
'''
Name: location_delete.py
Description: Delete location --location from netbox
'''
our_version = 100
import argparse

from lib.common import netbox
from lib.location import Location

help_location = 'Name of the location to delete.'

ex_prefix = ' Example: '
ex_location = '{} --location mylocation'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a location')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--location',
                     dest='location',
                     required=True,
                     help=help_location + ex_location)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.location
    return info

nb = netbox()
l = Location(nb, get_info())
l.delete()
