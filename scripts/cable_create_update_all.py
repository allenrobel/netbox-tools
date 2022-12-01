#!/usr/bin/env python3
"""
Name: cable_create_update_all.py
Description: Create/update all cables defined in ``--yaml``
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import netbox, load_yaml
from netbox_tools.cable import Cable

OUR_VERSION = 102


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing device type information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./cables.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update all cables defined in --yaml"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=help_yaml + ex_yaml
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


def get_device_from_interface_key(interface_key):
    """
    given an interface key, return the associated device name
    """
    if interface_key not in info["interfaces"]:
        interfaces = ",".join(info["interfaces"].keys())
        log(f"exiting. port_key {interface_key} not found in interfaces {interfaces}")
        sys.exit(1)
    if "device" not in info["interfaces"][interface_key]:
        log(
            "exiting.",
            f"device key not found in interface dict {info['interfaces'][interface_key]}",
        )
        sys.exit(1)
    return info["interfaces"][interface_key]["device"]


def get_interface_from_interface_key(interface_key):
    """
    given an interface key, return the associated interface name
    """
    if interface_key not in info["interfaces"]:
        interfaces = ",".join(info["interfaces"].keys())
        log(f"exiting. port_key {interface_key} not found in interfaces {interfaces}")
        sys.exit(1)
    if "interface" not in info["interfaces"][interface_key]:
        log(
            "exiting."
            f"interface key not found in interface dict {info['interfaces'][interface_key]}"
        )
        sys.exit(1)
    return info["interfaces"][interface_key]["interface"]


def make_args():
    """
    return the arguments dictionary expected by Cable()
    """
    args = {}
    if "cable_type" in info["cables"][key]:
        args["cable_type"] = info["cables"][key]["cable_type"]
    if "color" in info["cables"][key]:
        args["color"] = info["cables"][key]["color"]
    args["device_a"] = get_device_from_interface_key(info["cables"][key]["port_a"])
    args["device_b"] = get_device_from_interface_key(info["cables"][key]["port_b"])
    args["label"] = info["cables"][key]["label"]
    if "length" in info["cables"][key]:
        args["length"] = info["cables"][key]["length"]
    if "length_unit" in info["cables"][key]:
        args["length_unit"] = info["cables"][key]["length_unit"]
    args["port_a"] = get_interface_from_interface_key(info["cables"][key]["port_a"])
    args["port_b"] = get_interface_from_interface_key(info["cables"][key]["port_b"])
    args["port_a_type"] = "interface"
    args["port_b_type"] = "interface"
    if "tags" in info["cables"][key]:
        args["tags"] = info["cables"][key]["tags"]
    return args


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
for key in info["cables"]:
    cable = Cable(netbox_obj, make_args())
    cable.create_or_update()
