#!/usr/bin/env python3
'''
Name: device_choices_print.py
Description: print choices associated with dcim.devices
'''
import pynetbox
from lib.credentials import NetboxCredentials

def print_header():
    print(fmt.format(
        'key',
        'valid_values'))
    print(fmt.format(
        '-' * 15,
        '-' * 65))
def print_choices(items):
    for item in items:
        choices = list()
        for d in items[item]:
            choices.append(d['value'])
        print(fmt.format(item, ', '.join(choices)))

nc = NetboxCredentials()

netbox = pynetbox.api(nc.url, token=nc.token)
items = netbox.dcim.devices.choices()

fmt = '{:<15} {:<65}'
print_header()
print_choices(items)
