#!/usr/bin/env python3
'''
Name: device_print.py
Summary: Print the primary ipv4 address of a device
Description:
This can be used in bash scripts to ssh to devices.  For example:

#!/usr/bin/env bash
DEVICE=$1
SCRIPT="${HOME}/netbox-tools/device_print_mgmt_ip.py"
ssh admin@`${SCRIPT} --device $1`

'''
our_version = 101
import argparse
import json
import pynetbox
from netbox_tools.common import netbox

help_device = 'Name of device for which ipv4 address is to be printed.'

ex_prefix     = 'Example: '
ex_device = '{} --device cvd_leaf_3'.format(ex_prefix)

parser = argparse.ArgumentParser(
         description='DESCRIPTION: Print the primary ipv4 address of a device')

mandatory = parser.add_argument_group(title='MANDATORY SCRIPT ARGS')
default   = parser.add_argument_group(title='DEFAULT SCRIPT ARGS')

mandatory.add_argument('--device',
                     dest='device',
                     required=True,
                     help=help_device + ex_device)
parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {}'.format(our_version))

cfg = parser.parse_args()

fmt = '{:>5} {:<20} {:<30}'

def get_device():
    device = nb.dcim.devices.get(name=cfg.device)
    if device == None:
        print('Device {} does not exist in netbox.'.format(cfg.name))
        exit(1)
    return device

nb = netbox()
device = get_device()
ipv4 = device.primary_ip4.address.split('/')[0]
print(ipv4)
