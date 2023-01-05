#!/usr/bin/env python3
"""
Name: ip_address_delete.py
Description: Delete ip address ``--ip`` from netbox
"""
import argparse

from netbox_tools.common import netbox
from netbox_tools.ip_address import IpAddress

OUR_VERSION = 101


def get_parser():
    """
    return an argparse parser object
    """
    help_ip = "IP address to delete. Specify with format A.B.C.D/E"
    ex_prefix = " Example: "
    ex_ip = f"{ex_prefix} --ip 192.168.0.0/24"

    parser = argparse.ArgumentParser(description="DESCRIPTION: Delete ip address")

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    mandatory.add_argument("--ip", dest="ip", required=True, help=help_ip + ex_ip)

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_info():
    """
    return dictionary containing arguments expected by IpAddress
    """
    info = {}
    info["ip4"] = cfg.ip
    return info


cfg = get_parser()
nb = netbox()
p = IpAddress(nb, get_info())
p.delete()
