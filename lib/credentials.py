#!/usr/bin/env python
'''
Name: credentials.py
Description:

Read the caller's Ansible vault and expose the following keys via properties:

token - via property token
url - via property url

Dependencies:

1. Ansible libraries

Install with:

pip install ansible

2. NetboxLoadConfig()

In this repo at ./netbox_lib/config/netbox_config.py

NetboxLoadConfig() loads netbox-tools's settings, which includes the path to your
ansible vault.  To configure this path, edit netbox_tools/lib/config/netbox_config.py
and modify the config_file variable at the top of the file to point to your
vault e.g.

netbox_vault = /Users/arobel/repos/netbox-tools/lib/secrets
'''
from ansible import constants as C
from ansible.cli import CLI
from ansible.parsing.dataloader import DataLoader

from lib.config.netbox_config import LoadConfig

class NetboxCredentials(object):
    def __init__(self):
        self.mandatory_keys = set()
        self.mandatory_keys.add('token')
        self.mandatory_keys.add('url')

        self.c = LoadConfig()

        self.load_credentials()

    def load_credentials(self):
        try:
            loader = DataLoader()
            vault_secrets = CLI.setup_vault_secrets(loader=loader,
                        vault_ids=C.DEFAULT_VAULT_IDENTITY_LIST)
            loader.set_vault_secrets(vault_secrets)
            data = loader.load_from_file(self.c.config['vault'])
        except Exception as e:
            print('unable to load credentials in {}.'.format(self.c.config['vault']))
            print('Exception was: {}'.format(e))
            exit(1)

        for k in self.mandatory_keys:
            if k not in data:
                print('Exiting. vault is missing key {}'.format(k))
                exit(1)
        self.credentials = dict()
        self.credentials['token'] = str(data['token'])
        self.credentials['url'] = str(data['url'])
    @property
    def token(self):
        return self.credentials['token']
    @property
    def url(self):
        return self.credentials['url']
