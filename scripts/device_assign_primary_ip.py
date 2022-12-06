#!/usr/bin/env python3
"""
Name: device_assign_primary_ip.py
Description: Assign an ip address to a device and make this address the primary ip for the device

Example Usage
./device_assign_primary_ip.py --device bgw_1 --ipv4 192.168.1.6/24 --status active
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import interface_id, ip_address_id, netbox
from netbox_tools.device import (
    initialize_device_primary_ip,
    map_device_primary_ip,
    make_device_primary_ip,
)

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_device = "Device name to which the interface is bound."
    help_interface = "Name of the interface to which ipv4 address will be bound."
    help_ipv4 = "IPv4 address of the interface"

    ex_prefix = "Example: "
    ex_device = f"{ex_prefix} --device leaf_1"
    ex_interface = f"{ex_prefix} --interface mgmt0"
    ex_ipv4 = f"{ex_prefix} --ipv4 192.168.1.6/24"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Add an ipv4 address and bind to interface"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--device",
        dest="device",
        required=True,
        help=help_device + ex_device,
    )
    mandatory.add_argument(
        "--interface",
        dest="interface",
        required=True,
        help=help_interface + ex_interface,
    )
    mandatory.add_argument(
        "--ipv4",
        dest="ipv4",
        required=True,
        help=help_ipv4 + ex_ipv4,
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def log(*args):
    """
    simple logger
    """
    print(f"{stack()[1].function}(v{OUR_VERSION}): {' '.join(args)}")


def assign_primary_ip_to_device():
    """
    map an exiting ip4 address to a device and make it the device's primary ip
    """
    ipv4_id = ip_address_id(netbox_obj, cfg.ipv4)
    intf_id = interface_id(netbox_obj, cfg.device, cfg.interface)

    if ipv4_id is None:
        log(
            f"exiting. Address {cfg.ipv4} not found at {netbox_obj.base_url}"
        )
        sys.exit(1)
    if intf_id is None:
        log(
            "exiting.",
            f"Interface {cfg.interface} not found at {netbox_obj.base_url}",
        )
        sys.exit(1)
    initialize_device_primary_ip(netbox_obj, cfg.device)
    map_device_primary_ip(netbox_obj, cfg.device, cfg.interface, cfg.ipv4)
    make_device_primary_ip(netbox_obj, cfg.device, cfg.ipv4)


cfg = get_parser()
netbox_obj = netbox()
assign_primary_ip_to_device()
