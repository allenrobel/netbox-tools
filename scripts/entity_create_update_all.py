#!/usr/bin/env python3
"""
Name: entity_create_all.py
Description: Create/update all Netbox entities (console server ports, device types, etc) from
             information in --yaml
Detail:

This script creates (if not present in Netbox) or updates (if present in Netbox)
all entities within the YAML file pointed to with --yaml

See info.yml in the top-level directory of this repo for the YAML structure this script assumes.
"""
import argparse
from inspect import stack
import sys

from netbox_tools.cluster import Cluster
from netbox_tools.cluster_type import ClusterType
from netbox_tools.common import (
    netbox,
    load_yaml,
    make_ip_address_dict,
)
from netbox_tools.console_port import ConsolePort
from netbox_tools.console_server_port import ConsoleServerPort
from netbox_tools.device import Device
from netbox_tools.device_type import DeviceType
from netbox_tools.interface import Interface
from netbox_tools.ip_address import IpAddress
from netbox_tools.ip_prefix import IpPrefix
from netbox_tools.location import Location
from netbox_tools.manufacturer import Manufacturer
from netbox_tools.rack import Rack
from netbox_tools.role import Role
from netbox_tools.site import Site
from netbox_tools.tag import Tag
from netbox_tools.virtual_interface import VirtualInterface
from netbox_tools.virtual_ip_address import VirtualIpAddress
from netbox_tools.virtual_machine import VirtualMachine
from netbox_tools.vlan import Vlan
from netbox_tools.vlan_group import VlanGroup

OUR_VERSION = 106


def get_parser():
    """
    return an argparse instance
    """
    help_yaml = "JSON file to open (contains testbed info)"

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml /my/yaml/file.yml"

    parser = argparse.ArgumentParser(description="DESCRIPTION: Netbox: Delete a device")

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=help_yaml + ex_yaml
    )

    parser.add_argument(
        "--version", action="version", version=f"{'%(prog)s'} {OUR_VERSION}"
    )

    return parser.parse_args()


def log(*args):
    """
    simple logger
    """
    print(f"{stack()[1].function}(v{OUR_VERSION}): {' '.join(args)}")


def fix_deprecations():
    """
    A couple parameter names have changed. If the user is using the older
    parameter names, warn them and copy the values to the new names.

    TODO: Used for backward-compatibility. Remove after 2023-09-29
    """
    if "mgmt_interface" in info:
        log(
            "WARNING: devices: <device>: mgmt_interface in your YAML file is deprecated.",
            "Use devices: <device>: interface instead.",
        )
        info["interface"] = info["mgmt_interface"]
    if "name" in info:
        log(
            "WARNING: devices: <device>: name in your YAML file is deprecated.",
            "Use devices: <device>: device instead.",
        )
        info["device"] = info["name"]


def get_interface_dict(device_dict, interfaces_dict):
    """
    device_dict contains a pointer (interface) into interfaces_dict.
    Use this to lookup and return the corresponding interface configuration
    from the interfaces_dict.
    """
    if "interface" not in device_dict:
        log(f"exiting. interface key not found in device_dict {device_dict}")
        sys.exit(1)
    interface_key = device_dict["interface"]
    if interface_key not in interfaces_dict:
        log(
            "exiting",
            f"Interface {interface_key} not found in {cfg.yaml}",
            f"interfaces dictionary: {interfaces_dict.keys()}.",
        )
        sys.exit(1)
    return interfaces_dict[interface_key]


def devices_create_update(
    interfaces_dict, ip_addresses_dict, devices_dict, device_class
):
    """
    create or update device and set the device's primary_ip to
    its management interface ipv4 address
    """
    for device_key in devices_dict:
        device_obj = device_class(netbox_obj, devices_dict[device_key])
        device_obj.create_or_update()
        interface_dict = get_interface_dict(devices_dict[device_key], interfaces_dict)
        if "ip4" not in interface_dict:
            log(
                f"device {interface_dict['device']} interface {interface_dict['interface']}",
                "skipping ipv4 address processing since ip4 key is missing",
            )
            continue
        intf_obj = Interface(netbox_obj, interface_dict)
        intf_obj.create_or_update()
        ip_address_dict = make_ip_address_dict(ip_addresses_dict, interface_dict)
        ip4_obj = IpAddress(netbox_obj, ip_address_dict)
        ip4_obj.create_or_update()
        log("---")


def virtual_machines_create_update(
    interfaces_dict, ip_addresses_dict, vm_dict, virtual_machine_class
):
    """
    create or update virtual_machine and set the virtual_machine's
    primary_ip to its management interface ipv4 address
    """
    for vm_key in vm_dict:
        vm_obj = virtual_machine_class(netbox_obj, vm_dict[vm_key])
        vm_obj.create_or_update()
        interface_dict = get_interface_dict(vm_dict[vm_key], interfaces_dict)
        if "ip4" not in interface_dict:
            log(
                "skipping ipv4 address processing since ip4 key is missing:",
                f"virtual_machine {interface_dict['virtual_machine']}",
                f"interface {interface_dict['interface']}",
            )
            continue
        intf_obj = VirtualInterface(netbox_obj, interface_dict)
        intf_obj.create_or_update()
        ip_address_dict = make_ip_address_dict(ip_addresses_dict, interface_dict)
        vip_obj = VirtualIpAddress(netbox_obj, ip_address_dict)
        vip_obj.create_or_update()
        print("---")


def get_runner_dict():
    """
    return a dictionary, keyed on int(), that contains all the
    Netbox objects to create/update.  We key this on int() since
    the ordering of object creation matters.  For example, you
    cannot add tags to an object if the tag does not already exist
    in Netbox.
    """
    runner = {}
    runner[1] = {"key": "tags", "object": Tag}
    runner[2] = {"key": "sites", "object": Site}
    runner[3] = {"key": "locations", "object": Location}
    runner[4] = {"key": "manufacturers", "object": Manufacturer}
    runner[5] = {"key": "device_types", "object": DeviceType}
    runner[6] = {"key": "device_roles", "object": Role}
    runner[7] = {"key": "racks", "object": Rack}
    runner[8] = {"key": "prefixes", "object": IpPrefix}
    runner[9] = {"key": "vlan_groups", "object": VlanGroup}
    runner[10] = {"key": "vlans", "object": Vlan}
    runner[11] = {"key": "cluster_types", "object": ClusterType}
    runner[12] = {"key": "clusters", "object": Cluster}
    runner[13] = {"key": "devices", "object": Device}
    runner[14] = {"key": "console_server_ports", "object": ConsoleServerPort}
    runner[15] = {"key": "console_ports", "object": ConsolePort}
    runner[16] = {"key": "virtual_machines", "object": VirtualMachine}
    return runner


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
fix_deprecations()
runner_dict = get_runner_dict()
for item in sorted(runner_dict):
    print(f'--- {runner_dict[item]["key"]} ---')
    key = runner_dict[item]["key"]
    if key == "devices":
        # special case for devices
        devices_create_update(
            info["interfaces"],
            info["ip4_addresses"],
            info[key],
            runner_dict[item]["object"],
        )
        continue
    if key == "virtual_machines":
        # special case for virtual_machines
        virtual_machines_create_update(
            info["virtual_interfaces"],
            info["ip4_addresses"],
            info[key],
            runner_dict[item]["object"],
        )
        continue
    for entity in info[key]:
        obj = runner_dict[item]["object"](netbox_obj, info[key][entity])
        obj.create_or_update()
