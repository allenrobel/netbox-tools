#!/usr/bin/env python3
'''
Name: console_port_delete.py
Description: Delete console_port --port from netbox
'''
our_version = 100
import argparse

from netbox_tools.common import netbox
from netbox_tools.console_port import ConsolePort

def get_parser():
    help_device = 'Device containing the console_port to delete.'
    help_port = 'Name of the console_port to delete.'

    ex_prefix = ' Example: '
    ex_device = '{} --device mydevice'.format(ex_prefix)
    ex_port = '{} --port myconsole_port'.format(ex_prefix)

    parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a console_port')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--device',
                        dest='device',
                        required=True,
                        help=help_device + ex_device)
    mandatory.add_argument('--port',
                        dest='port',
                        required=True,
                        help=help_port + ex_port)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

def get_info():
    info = dict()
    info['port'] = cfg.port
    info['device'] = cfg.device
    return info

cfg = get_parser()
nb = netbox()
c = ConsolePort(nb, get_info())
c.delete()
