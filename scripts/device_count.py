#!/usr/bin/env python3
'''
Name: device_count.py
Description: Print the number of devices matching a given query

Multiple query parameters can be combined to and are boolean ANDed together for
greater specificity.

For example:

(py310) netbox-tools % ./device_count.py --site SJC03-1-155 --role leaf --model N9K-C93108TC-FX
Vault password: 
"Query: {'role': 'leaf', 'site': 'SJC03-1-155', 'model': 'N9K-C93108TC-FX'}"
Count: 1
(py310) netbox-tools % ./device_count.py --site SJC03-1-155 --role leaf                        
Vault password: 
"Query: {'role': 'leaf', 'site': 'SJC03-1-155'}"
Count: 10
(py310) netbox-tools % 

'''
our_version = 103
import argparse
import pprint

from netbox_tools.common import netbox

def get_parser():
    help_role = 'Filter on role.'
    help_site = 'Filter on site.'
    help_model = 'Filter on model number (e.g. N9K-C93180YC-EX).'

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

    return parser.parse_args()

def get_args():
    args = dict()
    if cfg.role != None:
        args['role'] = cfg.role
    if cfg.site != None:
        args['site'] = cfg.site
    if cfg.model != None:
        args['model'] = cfg.model
    return args

def verify_model():
    # 'device_type' does not work with count() for some reason.  We're using device_type.id as a workaround for now.
    models = dict()
    if cfg.model == None:
        return models
    items = nb.dcim.device_types.all()
    for item in items:
        models[item.model] = item.id
    if cfg.model in models.keys():
        return models
    else:
        print('Exiting. Model {} is not present in Netbox. Valid models: {}'.format(cfg.model, ', '.join(sorted(models))))
        exit(1)
def verify_role():
    roles = dict()
    if cfg.role == None:
        return roles
    items = nb.dcim.device_roles.all()
    for item in items:
        roles[item.name] = item.name
    if cfg.role in roles.keys():
        return roles
    else:
        print('Exiting. Role {} is not present in Netbox. Valid roles: {}'.format(cfg.role, ', '.join(sorted(roles.keys()))))
        exit(1)
def verify_site():
    # 'site' does not work with count() for some reason.  We're using site.id as a workaround for now.
    sites = dict()
    if cfg.site == None:
        return sites
    items = nb.dcim.sites.all()
    for item in items:
        sites[item.name] = item.id
    if cfg.site in sites.keys():
        return sites
    else:
        print('Exiting. Site {} is not present in Netbox. Valid sites: {}'.format(cfg.site, ', '.join(sorted(sites.keys()))))
        exit(1)

def get_device_count():
    models = verify_model()
    roles = verify_role()
    site_ids = verify_site()
    args = dict()
    try:
        if len(site_ids) != 0:
            args['site_id'] = site_ids[cfg.site]
        if len(roles) != 0:
            args['role'] = roles[cfg.role]
        if len(models.keys()) != 0:
            args['device_type_id'] = models[cfg.model]
        return nb.dcim.devices.count(**args)
    except Exception as e:
        print('Unable to get count: {}'.format(e))

cfg = get_parser()
nb = netbox()
count = get_device_count()
pprint.pprint('Query: {}'.format(get_args()))
print('Count: {}'.format(count))
