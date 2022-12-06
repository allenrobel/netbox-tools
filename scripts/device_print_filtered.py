#!/usr/bin/env python3
"""
Name: device_print_filtered.py
Summary: Print devices filtered by any/all of location, model, tags.
Description:

If --tags or --model are not provided, print all devices.
If --tags is provided, print devices that match the boolean ANDed set of tags.
If --model is provided, print devices that match model number.
If --location is provided, print devices that match device location.
If all arguments are provided, print devices that match the boolean ANDed result of all searches.

For example:

   --tags foo,bar,baz --model N9K-C9336C-FX2 --location row-v

Would match N9K-C9336C-FX2 that contain all three tags foo, bar, and baz and
that are located in row-v.
"""
import argparse
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_tags = "Comma-separated list of tags (no spaces)."
    help_tags += " If present, only devices containing tag(s) are printed."
    help_tags += " Else, all devices are printed."
    help_model = "Device model number"
    help_location = "Device location"

    ex_prefix = " Example: "
    ex_tags = f"{ex_prefix} --tags deathstar,admin"
    ex_model = f"{ex_prefix} --model N9K-C9336C-FX2"
    ex_location = f"{ex_prefix} --model N9K-C9336C-FX2"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Netbox: Print list of devices filtered by tag and/or model"
    )

    default = parser.add_argument_group(title="DEFAULT SCRIPT ARGS")

    default.add_argument(
        "--tags", dest="tags", required=False, help=f"{help_tags} {ex_tags}"
    )
    default.add_argument(
        "--location",
        dest="location",
        required=False,
        help=f"{help_location} {ex_location}",
    )
    default.add_argument(
        "--model", dest="model", required=False, help=f"{help_model} {ex_model}"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


def print_header():
    """
    print table header
    """
    print(
        FMT.format(
            "device_id",
            "name",
            "location",
            "model",
            "serial",
            "primary_ip4",
            "ip4_id",
            "status",
            "tags",
        )
    )
    print(
        FMT.format(
            "-" * 9,
            "-" * 18,
            "-" * 9,
            "-" * 18,
            "-" * 12,
            "-" * 22,
            "-" * 6,
            "-" * 10,
            "-" * 15,
        )
    )


def get_primary_ip(device_obj):
    """
    given a device object, return its primary_ip4
    return "na" if primary_ip4 is not mapped to the device.
    """
    if device_obj.primary_ip4 is None:
        return "na"
    return str(device_obj.primary_ip4)


def get_primary_ip_id(device_obj):
    """
    given a device object, return its primary_ip4's netbox ID.
    return "na" if primary_ip4 is not mapped to the device.
    """
    if device_obj.primary_ip4 is None:
        return "na"
    return device_obj.primary_ip4.id


def get_tags(device_obj):
    """
    given a device object, return the netbox tags associated
    with the device.
    return "" if no tags are associated with the device.
    """
    tags = device_obj.tags
    if tags is None:
        return ""
    return ",".join([tag.name for tag in device_obj.tags])


def print_matches(matches_dict):
    """
    given a dictionary of matches, keyed on device_name,
    print info associated with the matching device(s)
    """
    print_header()
    for device_name in matches_dict:
        if matches_dict[device_name] is False:
            continue
        device = matches_dict[device_name]
        print(
            FMT.format(
                device.id,
                device.name,
                str(device.location),
                device.device_type.model,
                device.serial,
                get_primary_ip(device),
                get_primary_ip_id(device),
                str(device.status),
                get_tags(device),
            )
        )


def unfiltered():
    """
    given a Netbox RecordSet of all devices return a dictionary, keyed on device name,
    whose values are the associated device objects.
    """
    matches_dict = {}
    for device in devices:
        matches_dict[device.name] = device
    return matches_dict


def filtered_on_tag():
    """
    Given the full set of devices from unfiltered(), return a dictionary, keyed on device name,
    whose values are set to False for all devices that do not contain one of tags the user
    is searching for.  If the value is already False, skip it since this means it didn't
    match a previous search (filtered_on_model()).
    """
    user_tags = set(cfg.tags.split(","))
    for device in matches:
        if matches[device] is False:
            continue
        device_tag_objects = matches[device].tags
        device_tags = set()
        for device_tag_object in device_tag_objects:
            device_tags.add(device_tag_object.name)
        if user_tags.issubset(device_tags):
            continue
        matches[device] = False
    return matches


def filtered_on_model():
    """
    Given the full set of devices from unfiltered(), return a dictionary, keyed on device name,
    whose values are set to False for all devices that do not match the device_type.model the user
    is searching for.  If the value is already False, skip it since this means it didn't
    match a previous search (e.g. filtered_on_model()).
    """
    for device in matches:
        if matches[device] is False:
            continue
        if matches[device].device_type.model != cfg.model:
            matches[device] = False
    return matches


def filtered_on_location():
    """
    Given the full set of devices from unfiltered(), return a dictionary, keyed on device name,
    whose values are set to False for all devices that do not match the device.location the user
    is searching for.  If the value is already False, skip it since this means it didn't
    match a previous search (e.g. filtered_on_model()).
    """
    for device in matches:
        if matches[device] is False:
            continue
        if str(matches[device].location) != cfg.location:
            matches[device] = False
    return matches


FMT = "{:<9} {:<18} {:<9} {:<18} {:<12} {:<22} {:<6} {:<10} {:<15}"

cfg = get_parser()
nb = netbox()
devices = nb.dcim.devices.all()

matches = unfiltered()
if cfg.tags is not None:
    matches = filtered_on_tag()
if cfg.model is not None:
    matches = filtered_on_model()
if cfg.location is not None:
    matches = filtered_on_location()

print_matches(matches)
