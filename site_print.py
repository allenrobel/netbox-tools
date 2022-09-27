#!/usr/bin/env python3
'''
Name: site_print.py
Description: Print information about a site
'''
our_version = 101
import argparse
import json
from lib.common import netbox

help_detail = 'Optional. If present, print detailed info about role.'
help_site = 'Retrieve information for site'

ex_prefix     = 'Example: '
ex_detail = '{} --detail'.format(ex_prefix)
ex_site = '{} --site fabric_1'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Print information about a site')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

default.add_argument('--detail',
                     dest='detail',
                     required=False,
                     default=False,
                     action='store_true',
                     help=help_detail + ex_detail)
mandatory.add_argument('--site',
                     dest='site',
                     required=True,
                     help=help_site + ex_site)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

fmt = '{:>5} {:<15} {:>12} {:>12} {:>12} {:<10} {:<30}'

def error():
    sites = list()
    items = nb.dcim.sites.all()
    for item in items:
        sites.append(item.name)
    print('site {} does not exist in netbox.  Valid sites: {}'.format(cfg.site, ', '.join(sites)))
    exit(1)
def get_site():
    site = nb.dcim.sites.get(name=cfg.site)
    if site == None:
        error()
    return site

def print_detail():
    pretty = json.dumps(dict(site), indent=4, sort_keys=True)
    print(pretty)

def print_headers():
    print(fmt.format('id', 'name', 'device_count', 'rack_count', 'prefix_count', 'status', 'description'))
    print(fmt.format('-' * 5, '-' * 15, '-' * 12, '-' * 12, '-' * 12, '-' * 10, '-' * 30))

nb = netbox()
site = get_site()
if cfg.detail:
    print_detail()
    exit()

print_headers()
print(fmt.format(site.id, site.name, site.device_count, site.rack_count, site.prefix_count, site.status.value, site.description))
