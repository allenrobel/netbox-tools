'''
netbox_config.py

Description:

Load YAML file pointed to by the config_file variable, and return the contents as a python dict()

Usage:

from netbox_tools.netbox_config import LoadConfig

c = LoadConfig()
print('c.vault {}'.format(c.config['vault']))

Author:

Allen Robel (arobel@cisco.com)
'''
import yaml

# EDIT THIS LINE TO POINT TO YOUR CONFIG FILE
config_file = '/home/myaccount/netbox-tools-prod/lib/netbox_tools/config/config.yml'
class LoadConfig(object):
    def __init__(self):
        self.properties = dict()
        self.load_config()

    def load_config(self):
        with open(config_file, 'r') as fp:
            self.properties['config'] = yaml.safe_load(fp)

    @property
    def config(self):
        return self.properties['config']
