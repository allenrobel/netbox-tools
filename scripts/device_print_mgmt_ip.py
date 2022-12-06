#!/usr/bin/env python3
"""
Name: device_print_mgmt_ip.py
Summary: Print the primary ipv4 address of a device
Description:
This can be used in bash scripts to ssh to devices.  For example:

#!/usr/bin/env bash
DEVICE=$1
SCRIPT="${HOME}/netbox-tools/device_print_mgmt_ip.py"
ssh admin@`${SCRIPT} --device $1`

"""
import argparse
import sys
from netbox_tools.common import netbox

OUR_VERSION = 103


def get_parser():
    """
    return an argparse parser object
    """
    help_device = "Name of device for which ipv4 address is to be printed."

    ex_prefix = "Example: "
    ex_device = f"{ex_prefix} --device cvd_leaf_3"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Print the primary ipv4 address of a device"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--device", dest="device", required=True, help=f"{help_device} {ex_device}"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_device_obj():
    """
    Return device object, if any, associated --device
    Exit if --device does not exist in user's netbox instance.
    """
    obj = netbox_obj.dcim.devices.get(name=cfg.device)
    if obj is None:
        print(f"Device {cfg.device} does not exist in netbox instance at {netbox_obj.base_url}.")
        sys.exit(1)
    return obj


FMT = "{:>5} {:<20} {:<30}"

cfg = get_parser()
netbox_obj = netbox()
device_obj = get_device_obj()
ip4 = device_obj.primary_ip4.address.split("/")[0]
print(ip4)
