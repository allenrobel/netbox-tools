#!/usr/bin/env python3
'''
Name: console_port_create_update_all.py
Description: Create/update all cables defined in ``--yaml``
'''
our_version = 100
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.console_port import ConsolePort

def get_parser():
    help_yaml = 'YAML file containing console_ports information.'

    ex_prefix     = 'Example: '
    ex_yaml = '{} --yaml ./console_ports.yml'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create/update all cables defined in ``--yaml``')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--yaml',
                        dest='yaml',
                        required=True,
                        help=help_yaml + ex_yaml)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

cfg = get_parser()
nb = netbox()
info = load_yaml(cfg.yaml)
for key in info['console_ports']:
    console_port = ConsolePort(nb, info['console_ports'][key])
    console_port.create_or_update()
