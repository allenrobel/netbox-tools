#!/usr/bin/env python3
"""
Name: device_count.py
Description: Print the number of devices matching a given query

Multiple query parameters can be combined and are boolean ANDed together.

For example:

(py310) netbox-tools % ./device_count.py --site S03-1-155 --role leaf --model N9K-C93108TC-FX
Vault password:
"Query: {'role': 'leaf', 'site': 'S03-1-155', 'model': 'N9K-C93108TC-FX'}"
Count: 1
(py310) netbox-tools % ./device_count.py --site S03-1-155 --role leaf
Vault password:
"Query: {'role': 'leaf', 'site': 'S03-1-155'}"
Count: 10
(py310) netbox-tools %

"""
import argparse
from inspect import stack
import sys
import pprint
from netbox_tools.common import netbox

OUR_VERSION = 104


def get_parser():
    """
    return an argparse parser object
    """
    help_role = "Filter on role."
    help_site = "Filter on site."
    help_model = "Filter on model number (e.g. N9K-C93180YC-EX)."

    ex_prefix = "Example: "
    ex_role = f"{ex_prefix} --role leaf"
    ex_site = f"{ex_prefix} --site f1"
    ex_model = f"{ex_prefix} --type N9K-C93180YC-EX"

    description = (
        "DESCRIPTION: Netbox: Count devices matching filters [role, site, model]."
    )
    description += " If no filter is provided, all devices are counted."
    description += " Filters are boolean ANDed together."

    parser = argparse.ArgumentParser(description=description)

    default = parser.add_argument_group(title="DEFAULT SCRIPT ARGS")

    default.add_argument(
        "--role",
        dest="role",
        required=False,
        default=None,
        help=f"{help_role} {ex_role}",
    )
    default.add_argument(
        "--site",
        dest="site",
        required=False,
        default=None,
        help=f"{help_site} {ex_site}",
    )
    default.add_argument(
        "--model",
        dest="model",
        required=False,
        default=None,
        help=f"{help_model} {ex_model}",
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


def get_args():
    """
    return a dictionary populated with the user's arguments
    key is the argument name
    value is the argument value
    """
    args = {}
    if cfg.role is not None:
        args["role"] = cfg.role
    if cfg.site is not None:
        args["site"] = cfg.site
    if cfg.model is not None:
        args["model"] = cfg.model
    return args


def verify_model():
    """
    return a dictionary of existing netbox device types.
    key is device type name, value is netbox device type id.
    dictionary will be empty if the user didn't specify --model

    Exit with error if the device type does not exist in netbox.

    NOTES:
    1. 'device_type' does not work with count() for some reason.
       We're using device_type.id as a workaround for now.
    """
    models = {}
    if cfg.model is None:
        return models
    items = netbox_obj.dcim.device_types.all()
    for item in items:
        models[item.model] = item.id
    if cfg.model in models:
        return models
    log(
        f"exiting. Model {cfg.model} is not present in Netbox.",
        f"Valid models: {', '.join(sorted(models))}",
    )
    sys.exit(1)


def verify_role():
    """
    return a dictionary of existing netbox device roles.
    key is device role name, value is netbox device role id.
    dictionary will be empty if the user didn't specify --role

    Exit with error if the device role does not exist in netbox.

    NOTES:
    1. 'role' does not work with count() for some reason.
       We're using role.id as a workaround for now.
    """
    roles = {}
    if cfg.role is None:
        return roles
    items = netbox_obj.dcim.device_roles.all()
    for item in items:
        roles[item.name] = item.id
    if cfg.role in roles:
        return roles
    log(
        f"exiting. Role {cfg.role} is not present in Netbox.",
        f"Valid roles: {', '.join(sorted(roles))}",
    )
    sys.exit(1)


def verify_site():
    """
    return a dictionary of existing netbox sites.
    key is site name, value is netbox site id.
    dictionary will be empty if the user didn't specify --site

    Exit with error if the device type does not exist in netbox.

    NOTES:
    1. 'site' does not work with count() for some reason.
       We're using site.id as a workaround for now.
    """
    sites = {}
    if cfg.site is None:
        return sites
    items = netbox_obj.dcim.sites.all()
    for item in items:
        sites[item.name] = item.id
    if cfg.site in sites:
        return sites
    log(
        f"exiting. Site {cfg.site} is not present in Netbox.",
        f"Valid sites: {', '.join(sorted(sites))}",
    )
    sys.exit(1)


def get_device_count():
    """
    return the number of devices matching a given query
    """
    models = verify_model()
    role_ids = verify_role()
    site_ids = verify_site()
    args = {}
    try:
        if len(site_ids) != 0:
            args["site_id"] = site_ids[cfg.site]
        if len(role_ids) != 0:
            args["role_id"] = role_ids[cfg.role]
        if len(models.keys()) != 0:
            args["device_type_id"] = models[cfg.model]
        return netbox_obj.dcim.devices.count(**args)
    except Exception as general_exception:
        log("Unable to get count.", f"Exception detail: {general_exception}")
        sys.exit(1)


cfg = get_parser()
netbox_obj = netbox()
count = get_device_count()
pprint.pprint(f"Query: {get_args()}")
print(f"Count: {count}")
