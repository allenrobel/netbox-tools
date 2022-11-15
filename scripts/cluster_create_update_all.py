#!/usr/bin/env python3
'''
Name: cluster_create_update_all.py
Description: Create/update clusters defined in ``--yaml`
'''
our_version = 100
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.cluster import Cluster

def get_parser():
    help_yaml = 'YAML file containing cluster type information.'

    ex_prefix     = 'Example: '
    ex_yaml = '{} --yaml ./clusters.yml'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create/update Netbox clusters defined in ``--yaml``')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--yaml',
                        dest='yaml',
                        required=True,
                        help=help_yaml + ex_yaml)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

cfg = get_parser()
nb = netbox()
info = load_yaml(cfg.yaml)
for key in info['clusters']:
    c = Cluster(nb, info['clusters'][key])
    c.create_or_update()
