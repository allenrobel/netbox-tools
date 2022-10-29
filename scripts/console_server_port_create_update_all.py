#!/usr/bin/env python3
'''
Name: console_server_port_create_update_all.py
Description: Create or update operations on Netbox endpoint /dcim/console-server-ports/ from information in a YAML file.
'''
our_version = 101
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.console_server_port import ConsoleServerPort

help_yaml = 'YAML file containing console_server_ports information.'

ex_prefix     = 'Example: '
ex_yaml = '{} --yaml ./console_server_ports.yml'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Create or update operations on Netbox endpoint /dcim/console-server-ports/ from information in a YAML file')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--yaml',
                     dest='yaml',
                     required=True,
                     help=help_yaml + ex_yaml)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

nb = netbox()
info = load_yaml(cfg.yaml)
for key in info['console_server_ports']:
    console_server_port = ConsoleServerPort(nb, info['console_server_ports'][key])
    console_server_port.create_or_update()
