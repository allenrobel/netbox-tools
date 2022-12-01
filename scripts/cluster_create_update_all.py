#!/usr/bin/env python3
"""
Name: cluster_create_update_all.py
Description: Create/update clusters defined in ``--yaml`
"""
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.cluster import Cluster

OUR_VERSION = 101


def get_parser():
    """
    return an argparse parser object
    """
    help_yaml = "YAML file containing cluster type information."

    ex_prefix = "Example: "
    ex_yaml = f"{ex_prefix} --yaml ./clusters.yml"

    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Create/update Netbox clusters defined in ``--yaml``"
    )

    mandatory = parser.add_argument_group(title="MANDATORY SCRIPT ARGS")

    mandatory.add_argument(
        "--yaml", dest="yaml", required=True, help=help_yaml + ex_yaml
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {OUR_VERSION}"
    )

    return parser.parse_args()


cfg = get_parser()
netbox_obj = netbox()
info = load_yaml(cfg.yaml)
for key in info["clusters"]:
    c = Cluster(netbox_obj, info["clusters"][key])
    c.create_or_update()
