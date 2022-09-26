#!/usr/bin/env python3
'''
Name: tag_create_all.py
Summary: Delete all tags contained in the YAML file pointed to with --yaml
Description: Delete tag --tag from netbox
'''
our_version = 101
import argparse
import pynetbox

from lib.credentials import NetboxCredentials
from lib.tag import Tag

help_tag = 'Name of the tag to delete.'

ex_prefix = ' Example: '
ex_tag = '{} --tag leaf_3'.format(ex_prefix)

parser = argparse.ArgumentParser(description='DESCRIPTION: Netbox: Delete a tag')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--tag',
                     dest='tag',
                     required=True,
                     help=help_tag + ex_tag)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_info():
    info = dict()
    info['name'] = cfg.tag
    return info

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)
d = Tag(nb, get_info())
d.delete()
