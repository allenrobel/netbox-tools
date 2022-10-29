#!/usr/bin/env python3
'''
Name: interface_delete.py
Description: Delete interface ``--interface`` from netbox
'''
our_version = 101
import argparse

from netbox_tools.common import netbox
from netbox_tools.interface import Interface

help_device = 'Name of the device associated with --interface'
help_interface = 'Name of the interface to delete.'

ex_prefix = ' Example: '
ex_device = '{} --device leaf_3'.format(ex_prefix)
ex_interface = '{} --interface mgmt0'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Delete interface --interface from netbox')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--device',
                     dest='device',
                     required=True,
                     help=help_device + ex_device)
mandatory.add_argument('--interface',
                     dest='interface',
                     required=True,
                     help=help_interface + ex_interface)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['interface'] = cfg.interface
    info['device'] = cfg.device
    return info

nb = netbox()
i = Interface(nb, get_info())
i.delete()
