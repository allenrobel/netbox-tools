#!/usr/bin/env python3
'''
Name: interface_create.py
Description: create an interface in netbox
Example Usage:
./interface_create.py --device bgw_1 --name mgmt0 --type 1000base-t --mgmt_only --enabled --mac 0844.cc4c.ee51
'''
our_version = 100
import pynetbox
import argparse

from lib.credentials import NetboxCredentials
from lib.interface import Interface

help_device = 'Device name to which the interface will be added.'
help_enabled = 'Optional. Is the interface enabled or not. Default is True (enabled)'
help_name = 'Name of the interface to add.'
help_mac = 'Optional. Mac address of the interface.'
help_mgmt_only = 'Optional. If present, interface will be flagged as management only. Default is False (not mgmt only)'
help_type = 'Type of interface to create (see http://<netbox_ip>/api/docs/ and look in POST /dcim/interfaces/ under type for valid types).'

ex_prefix = 'Example: '
ex_device = '{} --device leaf_1'.format(ex_prefix)
ex_enabled = '{} --enabled'.format(ex_prefix)
ex_name = '{} --name mgmt0'.format(ex_prefix)
ex_mac = '{} --mac 00:01:00:00:bd:ff'.format(ex_prefix)
ex_mgmt_only = '{} --mgmt_only'.format(ex_prefix)
ex_type = '{} --type 1000base-t'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Add a device')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--device',
                     dest='device',
                     required=True,
                     help=help_device + ex_device)

mandatory.add_argument('--name',
                     dest='name',
                     required=True,
                     help=help_name + ex_name)

mandatory.add_argument('--type',
                     dest='type',
                     required=False,
                     default=None,
                     help=help_type + ex_type)

default.add_argument('--enabled',
                     dest='enabled',
                     required=False,
                     default=False,
                     action='store_true',
                     help=help_enabled + ex_enabled)

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

def get_device_id():
    response = nb.dcim.devices.get(name=cfg.device)
    if response == None:
        print('Exiting. device {} not defined in netbox'.format(cfg.device))
        exit(1)
    return response.id

def get_args():
    '''
    Mandatory keys:
       name: name of the device
       mgmt_interface: name of the management interface
    Optional keys:
        interface_type: Netbox type of this interface (default is 1000base-t)
        mac_address: Mac address of this interface
        mgmt_only: If True, the interface is used only for accessing management functions
        interface_enabled: If True, Netbox will set its internal interface state to enabled
    '''
    args = dict()
    args['name'] = cfg.device
    args['mgmt_interface'] = cfg.name
    args['mgmt_only'] = cfg.mgmt_only
    args['interface_enabled'] = cfg.enabled
    if cfg.type != None:
        args['interface_type'] = cfg.type
    if cfg.mac != None:
        args['mac_address'] = cfg.mac
    return args

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)
i = Interface(nb, get_args())
i.create_or_update()