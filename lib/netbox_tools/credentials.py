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

from netbox_tools.config.netbox_config import LoadConfig

class NetboxCredentials(object):
    def __init__(self):
        self.mandatory_keys = set()
        self.mandatory_keys.add('netbox_token')
        self.mandatory_keys.add('netbox_url')

        # TODO: Remove deprecated keys handling after 2023-11-01
        self.deprecated_keys = set()
        self.deprecated_keys.add('token')
        self.deprecated_keys.add('url')

        self.c = LoadConfig()

        self.load_credentials()

    def verify_mandatory_keys(self):
        for k in self.mandatory_keys:
            if k not in self.data:
                return False
        return True
    def verify_deprecated_keys(self):
        # TODO: remove deprecated keys handling after 2023-11-01
        for k in self.deprecated_keys:
            if k not in self.data:
                return False
        return True
    def load_credentials(self):
        try:
            loader = DataLoader()
            vault_secrets = CLI.setup_vault_secrets(loader=loader,
                        vault_ids=C.DEFAULT_VAULT_IDENTITY_LIST)
            loader.set_vault_secrets(vault_secrets)
            self.data = loader.load_from_file(self.c.config['vault'])
        except Exception as e:
            print('unable to load credentials in {}.'.format(self.c.config['vault']))
            print('Exception was: {}'.format(e))
            exit(1)

        # TODO: remove deprecated keys handling after 2023-11-01
        use_deprecated_keys = False
        if self.verify_mandatory_keys() == False:
            if self.verify_deprecated_keys() == True:
                use_deprecated_keys = True
                print('WARNING: Using deprecated keys in {}'.format(self.c.config['vault']))
                print('Deprecated keys will stop working after 2023-11-01')
            else:
                print('Exiting. Vault is missing one or more of the following keys {}'.format(self.mandatory_keys))
                exit(1)
                    
        self.credentials = dict()
        if use_deprecated_keys == True:
            self.credentials['netbox_token'] = str(self.data['token'])
            self.credentials['netbox_url'] = str(self.data['url'])
        else:
            self.credentials['netbox_token'] = str(self.data['netbox_token'])
            self.credentials['netbox_url'] = str(self.data['netbox_url'])

    @property
    def token(self):
        return self.credentials['netbox_token']
    @property
    def url(self):
        return self.credentials['netbox_url']
