#!/usr/bin/env python3
'''
Name: ipam_prefixes_print.py
Description: Display all ip prefixes
'''
from netbox_tools.common import netbox

def get_fmt():
    return '{id:>6} {prefix:<18} {status:<10} {site:<15} {vrf:<10} {description:<25}'

class Default(dict):
    def __missing__(self, key):
        return '{'+key+'}'

def print_ip_prefixes():
    items = nb.ipam.prefixes.all()
    if items == None:
        print('print_ip_prefixes: exiting. no prefixes found in netbox')
        exit()
    fmt = get_fmt()
    for item in items:
        iid = item.id
        prefix = item.prefix
        status = item.status.label
        if item.site == None:
            site = 'na'
        else:
            site = item.site.name
        if item.vrf == None:
            vrf = 'na'
        else:
            vrf = item.vrf
        description = item.description
        print(fmt.format(id=iid, prefix=prefix, status=status, site=site, vrf=vrf, description=description))
def print_headers():
    fmt = get_fmt()
    print(fmt.format(id='id', prefix='prefix', status='status', site='site', vrf='vrf', description='description'))
    print(fmt.format(id='-' * 6, prefix='-' * 18, status='-' * 10, site='-' * 15, vrf='-' * 10, description='-' * 25))

nb = netbox()

print_headers()
print_ip_prefixes()
