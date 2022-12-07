#!/usr/bin/env python3
"""
Name: device_type_print.py
Description: Display information about a device type
"""
import argparse
from inspect import stack
import sys
import json
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_detail = "Optional. If present, display detailed info about the device_type."
    help_model = "Search for device_type based on value of device_type model."

    ex_prefix = " Example: "
    ex_detail = f"{ex_prefix} --detail"
    ex_model = f"{ex_prefix} --model N9K-C93180YC-EX"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Print information for a device type."
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")
    default = parser.add_argument_group(title="DEFAULT SCRIPT ARGS")

    mandatory.add_argument(
        "--model", dest="model", required=True, help=f"{help_model} {ex_model}"
    )

    default.add_argument(
        "--detail",
        dest="detail",
        required=False,
        default=False,
        action="store_true",
        help=f"{help_detail} {ex_detail}",
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


def error():
    """
    Handle case where device_type object is not present in Netbox.
    Throw the user a bone by printing a list of device_types that ARE present.
    """
    device_type_models = []
    items = netbox_obj.dcim.device_types.all()
    for item in items:
        device_type_models.append(item.model)
    log(
        f"Device type model {cfg.model} does not exist at {netbox_obj.base_url}.",
        f"Valid device type models: {', '.join(device_type_models)}",
    )
    sys.exit(1)


def get_device_type():
    """
    return device_type object associated with model
    """
    result = netbox_obj.dcim.device_types.get(model=cfg.model)
    if result is None:
        error()
    return result


def print_detail():
    """
    print json returned by Netbox for the device_type object
    """
    pretty = json.dumps(dict(device_type_obj), indent=4, sort_keys=True)
    print(pretty)


def print_headers():
    """
    print table headers
    """
    print(FMT.format("id", "device_type", "device_count", "manufacturer"))
    print(FMT.format("-" * 5, "-" * 15, "-" * 12, "-" * 20))


cfg = get_parser()
netbox_obj = netbox()
device_type_obj = get_device_type()
if cfg.detail:
    print_detail()
else:
    FMT = "{:>5} {:<15} {:>12} {:<20}"
    print_headers()
    print(
        FMT.format(
            device_type_obj.id,
            device_type_obj.model,
            device_type_obj.device_count,
            device_type_obj.manufacturer.name,
        )
    )
