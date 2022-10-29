#!/usr/bin/env python3
'''
Name: tag_delete.py
Description: Delete tag ``--tag``
'''
our_version = 104
import argparse

from netbox_tools.common import netbox
from netbox_tools.tag import Tag

help_tag = 'Name of the tag to delete.'

ex_prefix = ' Example: '
ex_tag = '{} --tag infra'.format(ex_prefix)

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

nb = netbox()
t = Tag(nb, get_info())
t.delete()