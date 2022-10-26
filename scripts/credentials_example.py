#!/usr/bin/env python3
'''
Name: credentials_example.py
Description: Demonstrates usage for the netbox credentials library in this repo
'''
from lib.credentials import NetboxCredentials

nc = NetboxCredentials()

print('token {}'.format(nc.token))
print('url {}'.format(nc.url))
