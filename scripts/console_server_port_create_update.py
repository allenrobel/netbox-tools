#!/usr/bin/env python3
'''
Name: console_server_port_create_update.py
Description: Create/update a console server port
Example Usage:
./console_server_port_create_update.py --device ts_1 --port 2003 --description "a special port" --tags admin,infra
'''
our_version = 106
import argparse
import re
from netbox_tools.common import netbox
from netbox_tools.console_server_port import ConsoleServerPort

def get_parser():
    help_description = 'Optional. Description of the console_server_port.'
    help_device = 'Device name to which the console_server_port (--port) will be added.'
    help_port = 'Console server port to create or update'
    help_tags = 'Optional. Comma-separated (no spaces) list of tags to associate with the console server port'

    ex_prefix = ' Example: '
    ex_description = '{} --description "this is a very special console server port"'.format(ex_prefix)
    ex_device = '{} --device ts_1'.format(ex_prefix)
    ex_port = '{} --port'.format(ex_prefix)
    ex_tags = '{} --tags admin,infra'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Netbox: Create/update a console server port')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    optional   = parser.add_argument_group(title='OPTIONAL SCRIPT ARGS')

    optional.add_argument('--description',
                        dest='description',
                        required=False,
                        default=None,
                        help=help_description + ex_description)

    mandatory.add_argument('--device',
                        dest='device',
                        required=True,
                        help=help_device + ex_device)

    mandatory.add_argument('--port',
                        dest='port',
                        required=True,
                        help=help_port + ex_port)

    optional.add_argument('--tags',
                        dest='tags',
                        required=False,
                        default=None,
                        help=help_tags + ex_tags)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

def get_args():
    '''
    Mandatory keys:
       device: name of the device
       port: name of the console port e.g. for Cisco terminal servers: 2005
    Optional keys:
        description: Free-form description for the console server port
        tags: Python list of tags to associate with the console server port
    '''
    args = dict()
    args['device'] = cfg.device
    args['port'] = cfg.port
    if cfg.description != None:
        args['description'] = cfg.description
    if cfg.tags != None:
        args['tags'] = re.split(',', cfg.tags)
    return args

cfg = get_parser()
nb= netbox()
c = ConsoleServerPort(nb, get_args())
c.create_or_update()
