#!/usr/bin/env python3
'''
Name: example_netbox_credentials
Description: Shows how to use the netbox credentials library in this repo
'''
from lib.credentials import NetboxCredentials

nc = NetboxCredentials()

print('token {}'.format(nc.token))
print('url {}'.format(nc.url))
