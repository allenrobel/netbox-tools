'''
Name: interface.py
Description: Class for create and update operations on netbox interfaces
'''

from lib.common import device_id

class Interface(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['mgmt_interface', 'name']
        self.optional_keys = ['interface_type', 'mac_address', 'mgmt_only', 'interface_enabled']
        self.default_interface_type = '1000base-t'
        self.default_interface_enabled = True
        self.validate_keys()
        self.generate_args()

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('interface.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['name'] = self.name
        self.args['device'] = device_id(self.nb, self.device)
        if self.args['device'] == None:
            print('Interface.generate_args: exiting. Device {} does not exist in netbox'.format(self.device))
            exit(1)
        if self.interface_type == None:
            self.args['type'] = self.default_interface_type
        else:
            self.args['type'] = self.interface_type
        if self.mac_address != None:
            self.args['mac_address'] = self.mac_address
        if self.mgmt_only == None:
            self.args['mgmt_only'] = True
        else:
            self.args['mgmt_only'] = self.mgmt_only
        if self.interface_enabled == None:
            self.args['enabled'] = self.default_interface_enabled
        else:
            self.args['enabled'] = self.interface_enabled

    def create(self):
        print('Interface.create: {}'.format(self.name))
        try:
            self.nb.dcim.interfaces.create(self.args)
        except Exception as e:
            print('Interface.create: exiting. Unable to create interface {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def update(self):
        print('Interface.update: {}'.format(self.name))
        self.args['id'] = self.interface_id
        try:
            self.interface.update(self.args)
        except Exception as e:
            print('Interface.update: Exiting. Unable to update interface {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def create_or_update(self):
        if self.interface == None:
            self.create()
        else:
            self.update()

    @property
    def device(self):
        return self.info['name']
    
    @property
    def interface(self):
        return self.nb.dcim.interfaces.get(
            device=self.device,
            name=self.name)

    @property
    def interface_enabled(self):
        if 'interface_enabled' in self.info:
            return self.info['interface_enabled']
        else:
            return None

    @property
    def interface_id(self):
        return self.interface.id

    @property
    def interface_type(self):
        if 'interface_type' in self.info:
            return self.info['interface_type']
        else:
            return None

    @property
    def name(self):
        return self.info['mgmt_interface']

    @property
    def mac_address(self):
        if 'mac_address' in self.info:
            return self.info['mac_address']
        else:
            return None

    @property
    def mgmt_only(self):
        if 'mgmt_only' in self.info:
            return self.info['mgmt_only']
        else:
            return None
