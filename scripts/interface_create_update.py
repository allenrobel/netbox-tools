#!/usr/bin/env python3
"""
Name: interface_create_update.py
Description: Create/update an interface
Example Usage:
./interface_create_update.py \
    --device bgw_1 \
    --interface mgmt0 \
    --type 1000base-t \
    --mgmt_only \
    --disabled \
    --mac 0844.cc4c.ee51 \
    --description "My interface" \
    --label "My interface"
"""
import argparse
from netbox_tools.common import netbox
from netbox_tools.interface import Interface

OUR_VERSION = 108


def get_parser():
    """
    return an argparse parser object
    """
    help_device = "Device name to which the interface will be added."
    help_duplex = "Optional. Valid values: auto, full, half."
    help_description = (
        "Optional. Free-form description to associate with the interface."
    )
    help_disabled = "Optional. Is the interface disabled or not."
    help_disabled += " Default is False (i.e. interface is enabled)"
    help_interface = "Name of the interface to add."
    help_label = "Optional. Physical label on the interface."
    help_mac = "Optional. Mac address of the interface."
    help_mode = "Mode of interface (see http://<netbox_ip>/api/docs/"
    help_mode += " and look in POST /dcim/interfaces/ under type for valid modes)."
    help_mgmt_only = (
        "Optional. If present, interface will be flagged as management only."
    )
    help_mgmt_only += " Default is False (not mgmt only)"
    help_mtu = "Optional. Maximum transfer unit of the interface, in bytes."
    help_type = "Type of interface to create (see http://<netbox_ip>/api/docs/ and look"
    help_type += " in POST /dcim/interfaces/ under type for valid types)."
    help_vlan = "Optional. Currently, vlan is associated with access interfaces only."

    ex_prefix = " Example: "
    ex_description = f"{ex_prefix} --description 'Server Vlan20'"
    ex_duplex = f"{ex_prefix} --duplex auto"
    ex_device = f"{ex_prefix} --device leaf_1"
    ex_disabled = f"{ex_prefix} --disabled"
    ex_interface = f"{ex_prefix} --interface mgmt0"
    ex_label = f"{ex_prefix} --label my_interface_label"
    ex_mac = f"{ex_prefix} --mac 00:01:00:00:bd:ff"
    ex_mgmt_only = f"{ex_prefix} --mgmt_only"
    ex_mode = f"{ex_prefix} --mode access"
    ex_mtu = f"{ex_prefix} --mtu 9216"
    ex_type = f"{ex_prefix} --type 1000base-t"
    ex_vlan = f"{ex_prefix} --vlan 10"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Create or update an interface"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    default = parser.add_argument_group(title="DEFAULT SCRIPT ARGS")

    default.add_argument(
        "--description",
        dest="description",
        required=False,
        default=None,
        help=f"{help_description} {ex_description}",
    )

    mandatory.add_argument(
        "--device", dest="device", required=True, help=f"{help_device} {ex_device}"
    )

    default.add_argument(
        "--duplex",
        dest="duplex",
        required=False,
        default=None,
        help=f"{help_duplex} {ex_duplex}",
    )

    mandatory.add_argument(
        "--interface",
        dest="interface",
        required=True,
        help=f"{help_interface} {ex_interface}",
    )

    mandatory.add_argument(
        "--type",
        dest="type",
        required=True,
        default=None,
        help=f"{help_type} {ex_type}",
    )

    default.add_argument(
        "--disabled",
        dest="disabled",
        required=False,
        default=False,
        action="store_true",
        help=f"{help_disabled} {ex_disabled}",
    )

    default.add_argument(
        "--label",
        dest="label",
        required=False,
        default=None,
        help=f"{help_label} {ex_label}",
    )

    default.add_argument(
        "--mac", dest="mac", required=False, default=None, help=f"{help_mac} {ex_mac}"
    )

    default.add_argument(
        "--mode",
        dest="mode",
        required=False,
        default=None,
        help=f"{help_mode} {ex_mode}",
    )

    default.add_argument(
        "--mgmt_only",
        dest="mgmt_only",
        required=False,
        default=False,
        action="store_true",
        help=f"{help_mgmt_only} {ex_mgmt_only}",
    )

    default.add_argument(
        "--mtu", dest="mtu", required=False, default=None, help=f"{help_mtu} {ex_mtu}"
    )

    default.add_argument(
        "--vlan",
        dest="vlan",
        required=False,
        default=None,
        help=f"{help_vlan} {ex_vlan}",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def get_args():
    """
    Mandatory keys:
       device: name of the device
       interface: name of the interface
    Optional keys:
        description: free-form description to associate with the interfacee
        duplex: duplex of this interface. Valid values: auto, half, full
        interface_enabled: If True, Netbox will set its internal interface state to enabled
        interface_mode: Mode for this interface: access, tagged, tagged-all
        interface_type: Netbox type of this interface (default is 1000base-t)
        label: physical label attached to the interface
        mac_address: Mac address of this interface
        mgmt_only: If True, the interface is used only for accessing management functions
        mtu: maximum transfer unit for the interface, in bytes
        vlan: Currently, vlan is applicable for access-mode interfaces only
    """
    args = {}
    if cfg.description is not None:
        args["description"] = cfg.description
    args["device"] = cfg.device
    if cfg.disabled is True:
        args["interface_enabled"] = False
    else:
        args["interface_enabled"] = True
    if cfg.duplex is not None:
        args["duplex"] = cfg.duplex
    args["interface"] = cfg.interface
    if cfg.label is not None:
        args["label"] = cfg.label
    if cfg.mac is not None:
        args["mac_address"] = cfg.mac
    if cfg.mgmt_only is True:
        args["mgmt_only"] = True
    else:
        args["mgmt_only"] = False
    if cfg.mode is not None:
        args["interface_mode"] = cfg.mode
    if cfg.mtu is not None:
        args["mtu"] = cfg.mtu
    if cfg.type is not None:
        args["interface_type"] = cfg.type
    if cfg.vlan is not None:
        args["untagged_vlan"] = cfg.vlan
    return args


cfg = get_parser()
netbox_obj = netbox()

interface_obj = Interface(netbox_obj, get_args())
interface_obj.create_or_update()
