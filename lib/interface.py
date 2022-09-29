'''
Name: interface.py
Description: Create, update, delete operations on netbox interfaces
'''

from lib.common import device_id

class Interface(object):
    def __init__(self, nb, info):
        self.version = 101
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_create_update_keys = ['interface', 'device']
        self.mandatory_delete_keys = ['interface', 'device']
        # optional_keys is just FYI.  It's not referenced anywhere.
        self.optional_keys = ['interface_type', 'mac_address', 'mgmt_only', 'interface_enabled']
        self.default_interface_type = '1000base-t'
        self.default_interface_enabled = True
        self.fix_deprecations()

    def fix_deprecations(self):
        if 'mgmt_interface' in self.info:
            print('Interface.fix_deprecations: WARNING: devices: <device>: mgmt_interface in your YAML file is deprecated. Use devices: <device>: interface instead.')
            self.info['interface'] = self.info['mgmt_interface']
        if 'name' in self.info:
            print('Interface.fix_deprecations: WARNING: devices: <device>: name is in your YAML file is deprecated. Use devices: <device>: device instead.')
            self.info['device'] = self.info['name']

    def validate_create_update_keys(self):
        for key in self.mandatory_create_update_keys:
            if key not in self.info:
                print('interface.validate_create_update_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_create_update_args(self):
        self.args['name'] = self.interface_name
        self.args['device'] = device_id(self.nb, self.device)
        if self.args['device'] == None:
            print('Interface.generate_create_update_args: exiting. Device {} does not exist in netbox'.format(self.device))
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

    def delete(self):
        print('Interface.delete: {}'.format(self.interface_name))
        self.validate_delete_keys()
        if self.interface == None:
            print('Interface.delete: Nothing to do, interface {} does not exist in netbox.'.format(self.interface_name))
            return
        try:
            self.device.delete()
        except Exception as e:
            print('Interface.delete: Exiting. Unable to delete interface {}.  Error was: {}'.format(self.interface_name, e))
            exit(1)

    def create(self):
        print('Interface.create: {}'.format(self.interface_name))
        try:
            self.nb.dcim.interfaces.create(self.args)
        except Exception as e:
            print('Interface.create: exiting. Unable to create interface {}.  Error was: {}'.format(self.interface_name, e))
            exit(1)

    def update(self):
        print('Interface.update: {}'.format(self.interface_name))
        self.args['id'] = self.interface_id
        try:
            self.interface.update(self.args)
        except Exception as e:
            print('Interface.update: Exiting. Unable to update interface {}.  Error was: {}'.format(self.interface_name, e))
            exit(1)

    def create_or_update(self):
        self.validate_create_update_keys()
        self.generate_create_update_args()
        if self.interface == None:
            self.create()
        else:
            self.update()

    @property
    def device(self):
        return self.info['device']

    @property
    def interface(self):
        return self.nb.dcim.interfaces.get(
            device=self.device,
            name=self.interface_name)

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
    def interface_name(self):
        return self.info['interface']

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
