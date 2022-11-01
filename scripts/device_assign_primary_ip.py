#!/usr/bin/env python3
'''
Name: device_assign_primary_ip.py
Description: Assign an ip address to a device and make this address the primary ip for the device

Example Usage
./device_assign_primary_ip.py --device bgw_1 --ipv4 192.168.1.6/24 --status active
'''
our_version = 103
import argparse
from netbox_tools.common import interface_id, ip_address_id, netbox
from netbox_tools.device import initialize_device_primary_ip, map_device_primary_ip, make_device_primary_ip

def get_parser():
    help_device = 'Device name to which the interface is bound.'
    help_interface = 'Name of the interface to which ipv4 address will be bound.'
    help_ipv4 = 'IPv4 address of the interface'
    help_status = 'Status of the ip address (active, deprecated, reserved)'

    ex_prefix = 'Example: '
    ex_device = '{} --device leaf_1'.format(ex_prefix)
    ex_interface = '{} --interface mgmt0'.format(ex_prefix)
    ex_ipv4 = '{} --ipv4 192.168.1.6/24'.format(ex_prefix)
    ex_status = '{} --status deprecated'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Netbox: Add an ipv4 address and bind to interface')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--device',
                        dest='device',
                        required=True,
                        help=help_device + ex_device,
                        )
    mandatory.add_argument('--interface',
                        dest='interface',
                        required=True,
                        help=help_interface + ex_interface,
                        )
    mandatory.add_argument('--ipv4',
                        dest='ipv4',
                        required=True,
                        help=help_ipv4 + ex_ipv4,
                        )

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

def assign_primary_ip_to_device():
    ipv4_id = ip_address_id(nb, cfg.ipv4)
    intf_id = interface_id(nb, cfg.device, cfg.interface)

    if ipv4_id == None:
        print('assign_primary_ip_to_device: Exiting. Address {} not found in netbox'.format(cfg.ipv4))
        exit(1)
    if intf_id == None:
        print('assign_primary_ip_to_device: Exiting. Interface {} not found in netbox'.format(cfg.interface))
        exit(1)
    initialize_device_primary_ip(nb, cfg.device)
    map_device_primary_ip(nb, cfg.device, cfg.interface, cfg.ipv4)
    make_device_primary_ip(nb, cfg.device, cfg.ipv4)

cfg = get_parser()
nb = netbox()
assign_primary_ip_to_device()
