#!/usr/bin/env python3
'''
Name: rack_delete.py
Description: Delete rack ``--rack``
'''
our_version = 100
import argparse

from lib.common import netbox
from lib.rack import Rack

help_rack = 'Name of the rack to delete.'

ex_prefix = ' Example: '
ex_rack = '{} --rack myrack'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a rack')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--rack',
                     dest='rack',
                     required=True,
                     help=help_rack + ex_rack)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.rack
    return info

nb = netbox()
d = Rack(nb, get_info())
d.delete()
