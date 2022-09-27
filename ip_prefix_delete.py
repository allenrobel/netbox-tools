#!/usr/bin/env python3
'''
Name: ip_prefix_delete.py
Summary: Delete ip prefix
Description: Delete ip prefix --prefix from netbox
'''
our_version = 100
import argparse

from lib.common import netbox
from lib.ip_prefix import IpPrefix

help_prefix = 'IP prefix to delete. Specify with format A.B.C.D/E'

ex_pfx = ' Example: '
ex_prefix = '{} --prefix 192.168.0.0/24'.format(ex_pfx)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a prefix')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--prefix',
                     dest='prefix',
                     required=True,
                     help=help_prefix + ex_prefix)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['prefix'] = cfg.prefix
    return info

nb = netbox()
p = IpPrefix(nb, get_info())
p.delete()
