#!/usr/bin/env python3
"""
Name: virtual_ip_address_create_update_all.py
Description: Create/update all Netbox virtual_ip_addresses (vm IPs) defined in ``--yaml``
"""
import argparse
from netbox_tools.common import netbox, load_yaml, make_ip_address_dict
from netbox_tools.virtual_ip_address import VirtualIpAddress

OUR_VERSION = 101


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file in which ip_address information can be found."

    ex_prefix = " Example: "
    ex_yaml = f"{ex_prefix} --yaml ./info.yml"

    desc = "DESCRIPTION: Create/update all Netbox virtual_ip_addresses (vm IPs)"
    desc += " defined in ``--yaml``"
    parser = argparse.ArgumentParser(description=desc)
    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=f"{help_yaml} {ex_yaml}"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )
    return parser.parse_args()


cfg = get_parser()
info = load_yaml(cfg.yaml)
nb = netbox()
for key in info["virtual_interfaces"]:
    if "ip4" not in info["virtual_interfaces"][key]:
        continue
    print("---")
    ip_address_dict = make_ip_address_dict(
        info["ip4_addresses"], info["virtual_interfaces"][key]
    )
    vip = VirtualIpAddress(nb, ip_address_dict)
    vip.create_or_update()
