#!/usr/bin/env python3
"""
Name: cluster_create_update_one.py
Description: Create/update cluster with key ``--key`` in file ``--yaml``
"""
import argparse
from inspect import stack
import sys
from netbox_tools.common import netbox, load_yaml
from netbox_tools.cluster import Cluster

OUR_VERSION = 101


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing cluster type information."
    help_key = "Key to create/update"

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./clusters.yml"
    ex_key = f"{ex_prefix} --key mykey "

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update cluster with key ``--key`` in file ``--yaml``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument("--key", dest="key", required=True, help=help_key + ex_key)

    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=help_yaml + ex_yaml
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(OUR_VERSION)
    )

    return parser.parse_args()


def log(*args):
    """
    simple logger
    """
    print(f"{stack()[1].function}(v{OUR_VERSION}): {' '.join(args)}")

cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
if cfg.key not in info["clusters"]:
    log(f"exiting. Nothing to do.  key {cfg.key} not found in yaml {cfg.yaml}")
    sys.exit(0)
c = Cluster(netbox_obj, info["clusters"][cfg.key])
c.create_or_update()
