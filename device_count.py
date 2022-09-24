#!/usr/bin/env python3
'''
Name: device_count.py
Description: Print the number of devices matching a given query
'''
our_version = 100
import argparse
import pprint
import pynetbox

from lib.credentials import NetboxCredentials

help_role = 'Filter on role.'
help_site = 'Filter on site.'
help_model = 'Filter on model number (e.g. N9K-C93180YC-EX. Case insensitive, so n9k-c93180yc-ex works too...).'

ex_prefix     = 'Example: '
ex_role = '{} --role leaf'.format(ex_prefix)
ex_site = '{} --site f1'.format(ex_prefix)
ex_model = '{} --type N9K-C93180YC-EX'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Netbox: Count devices matching filters [role, site, model].  If no filter is provided, all devices are counted.  Filters are boolean ANDed together.')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

default.add_argument('--role',
                     dest='role',
                     required=False,
                     default=None,
                     help=help_role + ex_role)
default.add_argument('--site',
                     dest='site',
                     required=False,
                     default=None,
                     help=help_site + ex_site)
default.add_argument('--model',
                     dest='model',
                     required=False,
                     default=None,
                     help=help_model + ex_model)

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

def get_args():
    args = dict()
    if cfg.role != None:
        args['role'] = cfg.role
    if cfg.site != None:
        args['site'] = cfg.site
    if cfg.model != None:
        args['model'] = cfg.model.lower()
    return args

def verify_model():
    if cfg.model == None:
        return
    items = nb.dcim.device_types.all()
    models = list()
    for item in items:
        models.append(item.slug)
    if cfg.model.lower() in models:
        return
    else:
        print('Exiting. Model {} is not present in Netbox. Valid models: {}'.format(cfg.model, ', '.join(sorted(models))))
        exit(1)
def verify_role():
    if cfg.role == None:
        return
    items = nb.dcim.device_roles.all()
    roles = list()
    for item in items:
        roles.append(item.slug)
    if cfg.role.lower() in roles:
        return
    else:
        print('Exiting. Role {} is not present in Netbox. Valid roles: {}'.format(cfg.role, ', '.join(sorted(roles))))
        exit(1)
def verify_site():
    if cfg.site == None:
        return
    items = nb.dcim.sites.all()
    sites = list()
    for item in items:
        sites.append(item.slug)
    if cfg.site.lower() in sites:
        return
    else:
        print('Exiting. Site {} is not present in Netbox. Valid sites: {}'.format(cfg.site, ', '.join(sorted(sites))))
        exit(1)

def get_device_count():
    args = get_args()
    verify_model()
    verify_site()
    verify_role()
    try:
        return nb.dcim.devices.count(**args)
    except Exception as e:
        print('Unable to get count: {}'.format(e))

nc = NetboxCredentials()
nb = pynetbox.api(nc.url, token=nc.token)
count = get_device_count()
pprint.pprint('Query: {}'.format(get_args()))
print('Count: {}'.format(count))
