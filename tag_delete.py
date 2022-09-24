#!/usr/bin/env python3
'''
Name: tag_delete.py
Description: Delete a tag
'''
our_version = 100
import argparse
import pynetbox
from lib.credentials import NetboxCredentials

help_name = 'Name of the tag to delete.'

ex_prefix     = 'Example: '
ex_name = '{} --name mytag'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Delete a tag')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--name',
                     dest='name',
                     required=True,
                     help=help_name + ex_name)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_tag():
    return nb.extras.tags.get(name=cfg.name)

def delete_tag():
    tag = get_tag()
    if tag == None:
        print('Exiting. tag {} does not exist in netbox.'.format(cfg.name))
        exit(1)
    if tag.delete():
        print('{} deleted'.format(cfg.name))
    else:
        print('Unable to delete {}'.format(cfg.name))

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)
delete_tag()
