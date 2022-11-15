#!/usr/bin/env python3
'''
Name: cable_create_update_one.py
Description: Create/update cable in Netbox with key ``--key`` in file ``--yaml``
'''
our_version = 101
import argparse
from netbox_tools.common import netbox, load_yaml
from netbox_tools.cable import Cable

def get_parser():
    help_yaml = 'YAML file containing cable information.'
    help_key = 'Key to create/update'

    ex_prefix     = 'Example: '
    ex_yaml = '{} --yaml ./cables.yml'.format(ex_prefix)
    ex_key = '{} --key mycable '.format(ex_prefix)

    parser = argparse.ArgumentParser(
            description='DESCRIPTION: Create/update cable in Netbox with key ``--key`` in file ``--yaml``')

    mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
    default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

    mandatory.add_argument('--key',
                        dest='key',
                        required=True,
                        help=help_key + ex_key)

    mandatory.add_argument('--yaml',
                        dest='yaml',
                        required=True,
                        help=help_yaml + ex_yaml)

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(our_version))

    return parser.parse_args()

def get_device_from_interface_key(info, interface_key):
    if interface_key not in info['interfaces']:
        print('get_device_port_from_port_key: exiting. port_key {} not found in interfaces {}'.format(
            ','.join(info['interfaces'].keys())
        ))
        exit(1)
    if 'device' not in info['interfaces'][interface_key]:
        print('get_device_port_from_port_key: exiting. device key not found in interface dict {}'.format(
            info['interfaces'][interface_key]
        ))
        exit(1)
    return info['interfaces'][interface_key]['device']

def get_interface_from_interface_key(info, interface_key):
    if interface_key not in info['interfaces']:
        print('get_device_port_from_port_key: exiting. port_key {} not found in interfaces {}'.format(
            ','.join(info['interfaces'].keys())
        ))
        exit(1)
    if 'interface' not in info['interfaces'][interface_key]:
        print('get_device_port_from_port_key: exiting. interface key not found in interface dict {}'.format(
            info['interfaces'][interface_key]
        ))
        exit(1)
    return info['interfaces'][interface_key]['interface']

def make_args(info, key):
    args = dict()
    if 'cable_type' in info['cables'][key]:
        args['cable_type'] = info['cables'][key]['cable_type']
    if 'color' in info['cables'][key]:
        args['color'] = info['cables'][key]['color']
    args['device_a'] = get_device_from_interface_key(info, info['cables'][key]['port_a'])
    args['device_b'] = get_device_from_interface_key(info, info['cables'][key]['port_b'])
    args['label'] = info['cables'][key]['label']
    if 'length' in info['cables'][key]:
        args['length'] = info['cables'][key]['length']
    if 'length_unit' in info['cables'][key]:
        args['length_unit'] = info['cables'][key]['length_unit']
    args['port_a'] = get_interface_from_interface_key(info, info['cables'][key]['port_a'])
    args['port_b'] = get_interface_from_interface_key(info, info['cables'][key]['port_b'])
    args['port_a_type'] = 'interface'
    args['port_b_type'] = 'interface'
    if 'tags' in info['cables'][key]:
        args['tags'] = info['cables'][key]['tags']
    return args

cfg = get_parser()
nb = netbox()
info = load_yaml(cfg.yaml)
if cfg.key not in info['cables']:
    print('exiting. Nothing to do.  key {} not found in yaml {}'.format(cfg.key, cfg.yaml))
    exit()
args = make_args(info, cfg.key)
cable = Cable(nb, args)
cable.create_or_update()
