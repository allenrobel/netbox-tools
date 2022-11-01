#!/usr/bin/env python3
'''
Name: rack_print.py
Description: Display information about ``--rack``
'''
our_version = 103
import argparse
import json
from netbox_tools.common import netbox

def get_parser():
    help_detail = 'Optional. If present, print detailed info about device.'
    help_rack = 'Name of the rack.'

    ex_prefix     = 'Example: '
    ex_detail = '{} --detail'.format(ex_prefix)
    ex_rack = '{} --rack V009'.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Display information about a rack')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    default.add_argument('--detail',
                        dest='detail',
                        required=False,
                        default=False,
                        action='store_true',
                        help=help_detail + ex_detail)
    mandatory.add_argument('--rack',
                        dest='rack',
                        required=True,
                        help=help_rack + ex_rack)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

def error():
    racks = list()
    items = nb.dcim.racks.all()
    for item in items:
        racks.append(item.name)
    print('Rack {} does not exist in netbox.  Valid racks: {}'.format(cfg.rack, ', '.join(racks)))
    exit(1)

def get_rack():
    rack = nb.dcim.racks.get(name=cfg.rack)
    if rack == None:
        error()
    return rack

def print_detail():
    pretty = json.dumps(dict(rack), indent=4, sort_keys=True)
    print(pretty)

def print_headers():
    print(fmt.format('id', 'name', 'site'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 15))

cfg = get_parser()
nb = netbox()
rack = get_rack()

fmt = '{:>5} {:>15} {:>15}'

if cfg.detail:
    print_detail()
    exit()

print_headers()
print(fmt.format(rack.id, rack.name, rack.site.name))
