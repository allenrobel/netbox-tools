#!/usr/bin/env python3
"""
Name: cable_delete_one.py
Description: Delete cable from Netbox with key ``--key`` in file ``--yaml``
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import netbox, load_yaml
from netbox_tools.cable import Cable

OUR_VERSION = 101


def get_parser():
    """
    return an argparse instance
    """
    help_yaml = "YAML file containing cable information."
    help_key = "Key to delete."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./cables.yml"
    ex_key = f"{ex_prefix} --key mycable"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Delete cable from Netbox with key ``--key`` in file ``--yaml``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=help_yaml + ex_yaml
    )

    mandatory.add_argument("--key", dest="key", required=True, help=help_key + ex_key)

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
            "exiting.",
            f"interface key not found in interface dict {info['interfaces'][interface_key]}",
        )
        sys.exit(1)
    return info["interfaces"][interface_key]["interface"]


def make_args(key):
    """
    return the arguments dictionary expected by Cable()
    """
    args = {}
    args["port_a_type"] = "interface"
    args["port_b_type"] = "interface"
    args["port_a"] = get_interface_from_interface_key(info["cables"][key]["port_a"])
    args["port_b"] = get_interface_from_interface_key(info["cables"][key]["port_b"])
    args["device_a"] = get_device_from_interface_key(info["cables"][key]["port_a"])
    args["device_b"] = get_device_from_interface_key(info["cables"][key]["port_b"])
    args["label"] = info["cables"][key]["label"]
    return args


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
if cfg.key not in info["cables"]:
    log(f"exiting. Nothing to do. key {cfg.key} not found in yaml {cfg.yaml}")
    sys.exit(0)
cable = Cable(netbox_obj, make_args(cfg.key))
cable.delete()
