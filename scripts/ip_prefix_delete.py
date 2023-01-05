#!/usr/bin/env python3
'''
Name: ip_prefix_delete.py
Description: Delete ip prefix ``--prefix`` from netbox
'''
OUR_VERSION = 102
import argparse

from netbox_tools.common import netbox
from netbox_tools.ip_prefix import IpPrefix

def get_parser():
    help_prefix = 'IP prefix to delete. Specify with format A.B.C.D/E'

    ex_pfx = ' Example: '
    ex_prefix = '{} --prefix 192.168.0.0/24'.format(ex_pfx)

    parser = argparse.ArgumentParser(description='DESCRIPTION: Delete ip prefix')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--prefix',
                        dest='prefix',
                        required=True,
                        help=help_prefix + ex_prefix)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(OUR_VERSION))

    return parser.parse_args()

def get_info():
    info = dict()
    info['prefix'] = cfg.prefix
    return info

cfg = get_parser()
nb = netbox()
p = IpPrefix(nb, get_info())
p.delete()
