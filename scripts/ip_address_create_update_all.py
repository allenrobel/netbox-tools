#!/usr/bin/env python3
"""
Name: ip_address_create_update_all.py
Description: Create/update all ip addresses defined in ``--yaml``
"""
import argparse
from netbox_tools.common import netbox, load_yaml, make_ip_address_dict
from netbox_tools.ip_address import IpAddress

OUR_VERSION = 101

def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file in which ip_address information can be found."

    ex_prefix = " Example: "
    ex_yaml = f"{ex_prefix} --yaml ./info.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update all ip addresses defined in ``--yaml``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=help_yaml + ex_yaml
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


cfg = get_parser()
info = load_yaml(cfg.yaml)
nb = netbox()
for key in info["interfaces"]:
    ip_address_dict = make_ip_address_dict(
        info["ip4_addresses"], info["interfaces"][key]
    )
    if ip_address_dict is None:
        continue
    print("---")
    ip = IpAddress(nb, ip_address_dict)
    ip.create_or_update()
