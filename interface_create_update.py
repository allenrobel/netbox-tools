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
from lib.interface import Interface

help_device = 'Device name to which the interface will be added.'
help_disabled = 'Optional. Is the interface disabled or not. Default is False (i.e. interface is enabled)'
help_interface = 'Name of the interface to add.'
help_mac = 'Optional. Mac address of the interface.'
help_mgmt_only = 'Optional. If present, interface will be flagged as management only. Default is False (not mgmt only)'
help_type = 'Type of interface to create (see http://<netbox_ip>/api/docs/ and look in POST /dcim/interfaces/ under type for valid types).'

ex_prefix = ' Example: '
ex_device = '{} --device leaf_1'.format(ex_prefix)
ex_disabled = '{} --disabled'.format(ex_prefix)
ex_interface = '{} --interface mgmt0'.format(ex_prefix)
ex_mac = '{} --mac 00:01:00:00:bd:ff'.format(ex_prefix)
ex_mgmt_only = '{} --mgmt_only'.format(ex_prefix)
ex_type = '{} --type 1000base-t'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Create or update an interface')

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

mandatory.add_argument('--type',
                     dest='type',
                     required=False,
                     default=None,
                     help=help_type + ex_type)

default.add_argument('--disabled',
                     dest='disabled',
                     required=False,
                     default=False,
                     action='store_true',
                     help=help_disabled + ex_disabled)

default.add_argument('--mac',
                     dest='mac',
                     required=False,
                     default=None,
                     help=help_mac + ex_mac)

default.add_argument('--mgmt_only',
                     dest='mgmt_only',
                     required=False,
                     default=False,
                     action='store_true',
                     help=help_mgmt_only + ex_mgmt_only)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_args():
    '''
    Mandatory keys:
       device: name of the device
       interface: name of the interface
    Optional keys:
        interface_type: Netbox type of this interface (default is 1000base-t)
        mac_address: Mac address of this interface
        mgmt_only: If True, the interface is used only for accessing management functions
        interface_enabled: If True, Netbox will set its internal interface state to enabled
    '''
    args = dict()
    args['device'] = cfg.device
    args['interface'] = cfg.interface
    if cfg.mgmt_only == True:
        args['mgmt_only'] = True
    else:
        args['mgmt_only'] = False
    if cfg.disabled == True:
        args['interface_enabled'] = False
    else:
        args['interface_enabled'] = True
    if cfg.type != None:
        args['interface_type'] = cfg.type
    if cfg.mac != None:
        args['mac_address'] = cfg.mac
    return args

nb= netbox()

i = Interface(nb, get_args())
i.create_or_update()