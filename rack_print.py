#!/usr/bin/env python3
'''
Name: rack_print.py
Description: Display information about a rack
'''
our_version = 100
import argparse
import pynetbox

from lib.credentials import NetboxCredentials

help_name = 'Name of the rack.'

ex_prefix     = 'Example: '
ex_name = '{} --name V009'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Display information about a rack')

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


def error():
    racks = list()
    items = nb.dcim.racks.all()
    for item in items:
        racks.append(item.name)
    print('Rack {} does not exist in netbox.  Valid racks: {}'.format(cfg.rack, ', '.join(racks)))
    exit(1)
def get_rack():
    rack = nb.dcim.racks.get(name=cfg.name)
    if rack == None:
        error()
    return rack

def print_headers():
    print(fmt.format('id', 'name', 'site'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 15))

fmt = '{:>5} {:>15} {:>15}'

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)

rack = get_rack()
if rack != None:
    print(dict(rack))
print_headers()
print(fmt.format(rack.id, rack.name, rack.site.name))
