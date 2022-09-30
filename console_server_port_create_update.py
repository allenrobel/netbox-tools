#!/usr/bin/env python3
'''
Name: interface_create_update.py
Description: Netbox: Create or update an interface
Example Usage:
./interface_create_update.py --device bgw_1 --interface mgmt0 --type 1000base-t --mgmt_only --disabled --mac 0844.cc4c.ee51
'''
our_version = 103
import argparse

from lib.common import netbox
from lib.console_server_port import ConsoleServerPort

help_device = 'Device name to which the console_server_port (--port) will be added.'
help_port = 'Console server port to create or update'
help_description = 'Optional. Description of the console_server_port.'

ex_prefix = ' Example: '
ex_device = '{} --device leaf_1'.format(ex_prefix)
ex_port = '{} --port'.format(ex_prefix)
ex_description = '{} --description "this is a very special console server port"'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Create or update a console server port')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
optional   = parser.add_argument_group(title='OPTIONAL SCRIPT ARGS')

mandatory.add_argument('--device',
                     dest='device',
                     required=True,
                     help=help_device + ex_device)

mandatory.add_argument('--port',
                     dest='port',
                     required=True,
                     help=help_port + ex_port)

optional.add_argument('--description',
                     dest='description',
                     required=False,
                     default=None,
                     help=help_description + ex_description)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_args():
    '''
    Mandatory keys:
       device: name of the device
       port: name of the console port e.g. for Cisco terminal servers: 2005
    Optional keys:
        description: Free-form description for the console server port
    '''
    args = dict()
    args['device'] = cfg.device
    args['port'] = cfg.port
    if cfg.description != None:
        args['description'] = cfg.description
    return args

nb= netbox()

c = ConsoleServerPort(nb, get_args())
c.create_or_update()