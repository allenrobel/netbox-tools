#!/usr/bin/env python
"""
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
"""
from inspect import stack
import sys
from ansible.cli import CLI
from ansible.parsing.dataloader import DataLoader

from netbox_tools.config.netbox_config import LoadConfig

OUR_VERSION = 102


class NetboxCredentials:
    """
    Read the caller's Ansible vault and expose the following keys via properties:

    token - via property token
    url - via property url
    """

    def __init__(self):
        self._classname = __class__.__name__
        self.lib_version = OUR_VERSION

        self._mandatory_keys = set()
        self._mandatory_keys.add("netbox_token")
        self._mandatory_keys.add("netbox_url")

        # TODO: Remove deprecated keys handling after 2023-11-01
        self._deprecated_keys = set()
        self._deprecated_keys.add("token")
        self._deprecated_keys.add("url")

        self._config = LoadConfig()

        self._load_credentials()

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _verify_mandatory_keys(self):
        """
        return True if all mandatory keys are set
        else, return False
        """
        for k in self._mandatory_keys:
            if k not in self.data:
                return False
        return True

    def _verify_deprecated_keys(self):
        """
        return True if any deprecated keys are being used.
        else, return False
        """
        # TODO: remove deprecated keys handling after 2023-11-01
        for k in self._deprecated_keys:
            if k not in self.data:
                return False
        return True

    def _load_credentials(self):
        """
        load credentials from ansible vault
        """
        try:
            loader = DataLoader()
            vault_secrets = CLI.setup_vault_secrets(loader=loader, vault_ids=[])
            loader.set_vault_secrets(vault_secrets)
            self.data = loader.load_from_file(self._config.config["vault"])
        except Exception as _general_error:
            self.log(
                f"unable to load credentials in {self._config.config['vault']}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

        # TODO: remove deprecated keys handling after 2023-11-01
        use_deprecated_keys = False
        if self._verify_mandatory_keys() is False:
            if self._verify_deprecated_keys() is True:
                use_deprecated_keys = True
                self.log(
                    f"WARNING: Using deprecated keys in {self._config.config['vault']}",
                    "Deprecated keys will stop working after 2023-11-01",
                )
            else:
                self.log(
                    "exiting. Vault is missing one or more of the following keys:",
                    f"{self._mandatory_keys}",
                )
                sys.exit(1)

        self._credentials = {}
        if use_deprecated_keys is True:
            self._credentials["netbox_token"] = str(self.data["token"])
            self._credentials["netbox_url"] = str(self.data["url"])
        else:
            self._credentials["netbox_token"] = str(self.data["netbox_token"])
            self._credentials["netbox_url"] = str(self.data["netbox_url"])

    @property
    def token(self):
        """
        Netbox API Token
        """
        return self._credentials["netbox_token"]

    @property
    def url(self):
        """
        Netbox URL
        """
        return self._credentials["netbox_url"]
