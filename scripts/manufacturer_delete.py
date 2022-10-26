#!/usr/bin/env python3
'''
Name: manufacturer_delete.py
Description: Delete manufacturer ``--manufacturer``
'''
our_version = 100
import argparse

from lib.common import netbox
from lib.manufacturer import Manufacturer

help_manufacturer = 'Name of the manufacturer to delete.'

ex_prefix = ' Example: '
ex_manufacturer = '{} --manufacturer mymanufacturer'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a manufacturer')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--manufacturer',
                     dest='manufacturer',
                     required=True,
                     help=help_manufacturer + ex_manufacturer)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.manufacturer
    return info

nb = netbox()
d = Manufacturer(nb, get_info())
d.delete()
