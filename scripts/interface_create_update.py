#!/usr/bin/env python3
'''
Name: interface_create_update.py
Description: Create/update an interface
Example Usage:
./interface_create_update.py --device bgw_1 --interface mgmt0 --type 1000base-t --mgmt_only --disabled --mac 0844.cc4c.ee51 --description "My interface"
'''
our_version = 106
import argparse

from netbox_tools.common import netbox
from netbox_tools.interface import Interface

def get_parser():
    help_device = 'Device name to which the interface will be added.'
    help_description = 'Optional. Free-form description to associate with the interface.'
    help_disabled = 'Optional. Is the interface disabled or not. Default is False (i.e. interface is enabled)'
    help_interface = 'Name of the interface to add.'
    help_mac = 'Optional. Mac address of the interface.'
    help_mode = 'Mode of interface (see http://<netbox_ip>/api/docs/ and look in POST /dcim/interfaces/ under type for valid modes).'
    help_mgmt_only = 'Optional. If present, interface will be flagged as management only. Default is False (not mgmt only)'
    help_mtu = 'Optional. Maximum transfer unit of the interface, in bytes.'
    help_type = 'Type of interface to create (see http://<netbox_ip>/api/docs/ and look in POST /dcim/interfaces/ under type for valid types).'
    help_vlan = 'Optional. Currently, vlan is associated with access interfaces only.'

    ex_prefix = ' Example: '
    ex_description = '{} --description "Server Vlan20"'.format(ex_prefix)
    ex_device = '{} --device leaf_1'.format(ex_prefix)
    ex_disabled = '{} --disabled'.format(ex_prefix)
    ex_interface = '{} --interface mgmt0'.format(ex_prefix)
    ex_mac = '{} --mac 00:01:00:00:bd:ff'.format(ex_prefix)
    ex_mgmt_only = '{} --mgmt_only'.format(ex_prefix)
    ex_mode = '{} --mode access'.format(ex_prefix)
    ex_mtu = '{} --mtu 9216'.format(ex_prefix)
    ex_type = '{} --type 1000base-t'.format(ex_prefix)
    ex_vlan = '{} --vlan 10'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Netbox: Create or update an interface')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    default.add_argument('--description',
                        dest='description',
                        required=False,
                        default=None,
                        help=help_description + ex_description)

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

    default.add_argument('--mode',
                        dest='mode',
                        required=False,
                        default=None,
                        help=help_mode + ex_mode)

    default.add_argument('--mgmt_only',
                        dest='mgmt_only',
                        required=False,
                        default=False,
                        action='store_true',
                        help=help_mgmt_only + ex_mgmt_only)

    default.add_argument('--mtu',
                        dest='mtu',
                        required=False,
                        default=None,
                        help=help_mtu + ex_mtu)

    default.add_argument('--vlan',
                        dest='vlan',
                        required=False,
                        default=None,
                        help=help_vlan + ex_vlan)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

def get_args():
    '''
    Mandatory keys:
       device: name of the device
       interface: name of the interface
    Optional keys:
        description: free-form description to associate with the interfacee
        interface_enabled: If True, Netbox will set its internal interface state to enabled
        interface_mode: Mode for this interface: access, tagged, tagged-all
        interface_type: Netbox type of this interface (default is 1000base-t)
        mac_address: Mac address of this interface
        mgmt_only: If True, the interface is used only for accessing management functions
        mtu: maximum transfer unit for the interface, in bytes
        vlan: Currently, vlan is applicable for access-mode interfaces only
    '''
    args = dict()
    args['device'] = cfg.device
    args['interface'] = cfg.interface
    if cfg.description != None:
        args['description'] = cfg.description
    if cfg.mgmt_only == True:
        args['mgmt_only'] = True
    else:
        args['mgmt_only'] = False
    if cfg.mtu != None:
        args['mtu'] = cfg.mtu
    if cfg.disabled == True:
        args['interface_enabled'] = False
    else:
        args['interface_enabled'] = True
    if cfg.type != None:
        args['interface_type'] = cfg.type
    if cfg.mac != None:
        args['mac_address'] = cfg.mac
    if cfg.mode != None:
        args['interface_mode'] = cfg.mode
    if cfg.vlan != None:
        args['untagged_vlan'] = cfg.vlan
    return args

cfg = get_parser()
nb= netbox()

i = Interface(nb, get_args())
i.create_or_update()
