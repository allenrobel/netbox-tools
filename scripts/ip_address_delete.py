#!/usr/bin/env python3
'''
Name: ip_address_delete.py
Description: Delete ip address ``--ip`` from netbox
'''
our_version = 100
import argparse

from netbox_tools.common import netbox
from netbox_tools.ip_address import IpAddress

def get_parser():
    help_ip = 'IP address to delete. Specify with format A.B.C.D/E'

    ex_prefix = ' Example: '
    ex_ip = '{} --ip 192.168.0.0/24'.format(ex_prefix)

    parser = argparse.ArgumentParser(description='DESCRIPTION: Delete ip address')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--ip',
                        dest='ip',
                        required=True,
                        help=help_ip + ex_ip)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

def get_info():
    info = dict()
    info['ip4'] = cfg.ip
    return info

cfg = get_parser()
nb = netbox()
p = IpAddress(nb, get_info())
p.delete()
