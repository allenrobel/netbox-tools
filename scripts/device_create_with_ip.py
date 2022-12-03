#!/usr/bin/env python3
"""
Name: device_create_with_ip.py
Description: Create netbox device with primary ip using commmand-line arguments
See also: device_create_update_all.py, device_create_update_one.py

This script does the following:
  1. Create, or update, device
  2. Create management interface for the device
  3. Add IPv4 address to management interface
  4. Make IPv4 address the primary_ip for device

example_dict usage:

./device_create_with_ip.py \
    --device cvd_spine_3 \
    --interface cvd_spine_3_mgmt0 \
    --ip4 172.22.150.114/24 \
    --device_role spine \
    --site SJC03-1-155 \
    --interface_role vip \
    --device_type N9K-C9504 \
    --interface_type 1000base-t

"""
import argparse
from inspect import stack
import pynetbox

from netbox_tools.device import Device
from netbox_tools.interface import Interface
from netbox_tools.ip_address import IpAddress
from netbox_tools.credentials import NetboxCredentials

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_dict = {}
    help_dict["device"] = "Name of the device to add."
    help_dict["interface"] = "Management interface for the device."
    help_dict["interface_type"] = "PHY type for the device management interface."
    help_dict["ip4"] = "Management IPv4 address for the device."
    help_dict[
        "device_role"
    ] = "Role for the device. Device role must already exist in netbox."
    help_dict[
        "interface_role"
    ] = "Role for the interface. Netbox requires specific interface roles."
    help_dict["serial"] = "Optional. Default: na. Serial number of the device."
    help_dict[
        "site"
    ] = "Site in which device will reside. Site must already exist in netbox."
    help_dict[
        "tags"
    ] = "Optional comma-separated list of pre-existing tags associated with device."
    help_dict["tags"] += "All tags must already exist in netbox."
    help_dict[
        "device_type"
    ] = "Type of device (i.e. model number). model number must already exist in netbox"
    ex_prefix = "example_dict: "
    example_dict = {}
    example_dict["device"] = f"{ex_prefix} --device leaf_3"
    example_dict["device_role"] = f"{ex_prefix} --device_role leaf"
    example_dict["device_type"] = f"{ex_prefix} --device_type N9K-C93180YC-EX"
    example_dict["interface"] = f"{ex_prefix} --interface mgmt0"
    example_dict["interface_role"] = f"{ex_prefix} --interface_role loopback"
    example_dict["interface_type"] = f"{ex_prefix} --interface_type 1000base-t"
    example_dict["ip4"] = f"{ex_prefix} --ip4 192.168.1.5/24"
    example_dict["serial"] = f"{ex_prefix} --serial CX045BN"
    example_dict["site"] = f"{ex_prefix} --site f1"
    example_dict["tags"] = f"{ex_prefix} --tags poc,admin"

    parser = argparse.ArgumentParser(description="DESCRIPTION: Netbox: Add a device")

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    default = parser.add_argument_group(title="DEFAULT SCRIPT ARGS")

    mandatory.add_argument(
        "--device",
        dest="device",
        required=True,
        help=f"{help_dict['device']} {example_dict['device']}",
    )
    mandatory.add_argument(
        "--interface",
        dest="interface",
        required=True,
        help=f"{help_dict['interface']} {example_dict['interface']}",
    )
    mandatory.add_argument(
        "--interface_type",
        dest="interface_type",
        required=True,
        help=f"{help_dict['interface_type']} {example_dict['interface_type']}",
    )
    mandatory.add_argument(
        "--ip4",
        dest="ip4",
        required=True,
        help=f"{help_dict['ip4']} {example_dict['ip4']}",
    )
    mandatory.add_argument(
        "--device_role",
        dest="device_role",
        required=True,
        help=f"{help_dict['device_role']} {example_dict['device_role']}",
    )
    mandatory.add_argument(
        "--interface_role",
        dest="interface_role",
        required=True,
        help=f"{help_dict['interface_role']} {example_dict['interface_role']}",
    )
    default.add_argument(
        "--serial",
        dest="serial",
        required=False,
        default=None,
        help=f"{help_dict['serial']} {example_dict['serial']}",
    )
    mandatory.add_argument(
        "--site",
        dest="site",
        required=True,
        help=f"{help_dict['site']} {example_dict['site']}",
    )
    default.add_argument(
        "--tags",
        dest="tags",
        required=False,
        default=None,
        help=f"{help_dict['tags']} {example_dict['tags']}",
    )
    mandatory.add_argument(
        "--device_type",
        dest="device_type",
        required=True,
        help=f"{help_dict['device_type']} {example_dict['device_type']}",
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


def get_tags():
    """
    return the list of tags set by the user
    """
    tags = []
    for tag in cfg.tags.split(","):
        tags.append(tag)
    return tags


def get_device_info():
    """
    return a dictionary containing parameters expected by Device.
    """
    info = {}
    info["ip4"] = cfg.ip4
    info["interface"] = cfg.interface
    info["interface_type"] = cfg.interface_type
    info["device"] = cfg.device
    info["role"] = cfg.device_role
    if cfg.serial is not None:
        info["serial"] = cfg.serial
    else:
        cfg.serial = "na"
    info["site"] = cfg.site
    if cfg.tags is not None:
        info["tags"] = get_tags()
    info["type"] = cfg.device_type
    return info


def get_interface_info():
    """
    return a dictionary containing parameters expected by Interface
    """
    info = {}
    info["ip4"] = cfg.ip4
    info["interface"] = cfg.interface
    info["interface_type"] = cfg.interface_type
    info["device"] = cfg.device
    info["role"] = cfg.interface_role
    if cfg.serial is not None:
        info["serial"] = cfg.serial
    else:
        cfg.serial = "na"
    info["site"] = cfg.site
    if cfg.tags is not None:
        info["tags"] = get_tags()
    info["type"] = cfg.interface_type
    return info


def get_ip_address_info():
    """
    return dictionary with parameters expected by IpAddress class
    """
    info = {}
    info["ip4"] = cfg.ip4
    info["interface"] = cfg.interface
    info["device"] = cfg.device
    return info


cfg = get_parser()
netbox_credentials_obj = NetboxCredentials()
netbox_obj = pynetbox.api(
    netbox_credentials_obj.url, token=netbox_credentials_obj.token
)

device_info_dict = get_device_info()
interface_info_dict = get_interface_info()
ip_address_info_dict = get_ip_address_info()
print("---")
device_obj = Device(netbox_obj, device_info_dict)
device_obj.create_or_update()
interface_obj = Interface(netbox_obj, interface_info_dict)
interface_obj.create_or_update()
ip_address_obj = IpAddress(netbox_obj, ip_address_info_dict)
ip_address_obj.create_or_update()
