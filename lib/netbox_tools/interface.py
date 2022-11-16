'''
Name: interface.py
Description: Create, update, delete operations on netbox interfaces
'''
our_version = 103
from inspect import stack, getframeinfo, currentframe
from netbox_tools.common import device_id, netbox_id_untagged_vlan

class Interface(object):
    def __init__(self, nb, info):
        self.lib_version = our_version
        self.classname = __class__.__name__
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_create_update_keys = ['interface', 'device']
        self.mandatory_delete_keys = ['interface', 'device']
        # optional_keys is just FYI.  It's not used anywhere.
        self.optional_keys = set()
        self.optional_keys.add('description')
        self.optional_keys.add('duplex')              # str - half, full, auto
        self.optional_keys.add('interface_enabled')   # bool - is the interface enabled
        self.optional_keys.add('interface_mode')      # str - access, tagged, tagged-all
        self.optional_keys.add('interface_type')      # str - interface PHY type
        self.optional_keys.add('label')               # str - physical label
        self.optional_keys.add('mac_address')         # str - interface mac address
        self.optional_keys.add('mgmt_only')           # bool - is the interface only used for management
        self.optional_keys.add('mtu')
        self.optional_keys.add('untagged_vlan')
        self.default_interface_type = '1000base-t'
        self.default_interface_mode = 'access'
        self.default_interface_enabled = True
        self.default_mgmt_only = False
        self.fix_deprecations()
        self.populate_valid_choices()


    def log(self, msg):
        print('{}(v{}).{}: {}'.format(self.classname, self.lib_version, stack()[1].function, msg))


    def populate_valid_choices(self):
        self.valid_choices = dict()
        choices_dict = self.nb.dcim.interfaces.choices()
        for item in choices_dict:
            valid_values = choices_dict[item]
            self.valid_choices[item] = [item['value'] for item in valid_values]


    def fix_deprecations(self):
        if 'mgmt_interface' in self.info:
            self.log('WARNING: devices: <device>: mgmt_interface in your YAML file is deprecated. Use devices: <device>: interface instead.')
            self.info['interface'] = self.info['mgmt_interface']
        if 'name' in self.info:
            self.log('WARNING: devices: <device>: name in your YAML file is deprecated. Use devices: <device>: device instead.')
            self.info['device'] = self.info['name']


    def validate_delete_keys(self):
        for key in self.mandatory_delete_keys:
            if key not in self.info:
                self.log('exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)


    def validate_create_update_keys(self):
        for key in self.mandatory_create_update_keys:
            if key not in self.info:
                self.log('exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)


    def set_description(self):
        if self.description != None:
            self.args['description'] = self.description


    def set_device(self):
        self.args['device'] = device_id(self.nb, self.device)
        if self.args['device'] == None:
            self.log('exiting. Device {} does not exist in netbox'.format(self.device))
            exit(1)


    def set_duplex(self):
        if self.duplex == None:
            return
        if self.duplex in self.valid_choices['duplex']:
            self.args['duplex'] = self.duplex
        else:
            self.log('exiting. Invalid duplex. Got {}. Expected one of {}.'.format(
                self.duplex,
                ','.join(sorted(self.valid_choices['duplex']))))
            exit(1)


    def set_interface_enabled(self):
        if isinstance(self.interface_enabled, bool):
            self.args['enabled'] = self.interface_enabled
        elif self.interface_enabled == None:
            self.args['enabled'] = self.default_interface_enabled
        else:
            self.log('exiting. Invalid value for interface_enabled. Got {}. Expected boolean.'.format(
                self.interface_enabled))
            exit(1)


    def set_interface_mode(self):
        if self.interface_mode == None:
            return
        if self.interface_mode in self.valid_choices['mode']:
            self.args['mode'] = self.interface_mode
        else:
            self.log('exiting. Invalid interface_mode. Got {}. Expected one of {}.'.format(
                self.interface_mode,
                ','.join(sorted(self.valid_choices['mode']))))
            exit(1)


    def set_interface_type(self):
        if self.interface_type == None:
            self.log('exiting. missing required argument: interface_type')
            exit(1)
        if self.interface_type in self.valid_choices['type']:
            self.args['type'] = self.interface_type
        else:
            self.log('exiting. Invalid interface_type. Got {}. Expected one of {}.'.format(
                self.interface_type,
                ','.join(sorted(self.valid_choices['type']))))
            exit(1)


    def set_label(self):
        if self.label != None:
            self.args['label'] = self.label


    def set_mac_address(self):
        if self.mac_address != None:
            self.args['mac_address'] = self.mac_address


    def set_mgmt_only(self):
        if isinstance(self.mgmt_only, bool):
            self.args['mgmt_only'] = self.mgmt_only
        elif self.mgmt_only == None:
            self.args['mgmt_only'] = self.default_mgmt_only
        else:
            self.log('exiting. Invalid value for mgmt_only. Got {}. Expected boolean.'.format(
                self.mgmt_only))
            exit(1)


    def set_mtu(self):
        if self.mtu != None:
            self.args['mtu'] = self.mtu


    def set_untagged_vlan(self):
        if self.untagged_vlan != None:
            self.args['untagged_vlan'] = netbox_id_untagged_vlan(self.nb, self.untagged_vlan)


    def generate_create_update_args(self):
        self.args['name'] = self.interface
        self.set_description()
        self.set_device()
        self.set_duplex()
        self.set_interface_enabled()
        self.set_interface_mode()
        self.set_interface_type()
        self.set_label()
        self.set_mac_address()
        self.set_mgmt_only()
        self.set_mtu()
        self.set_untagged_vlan()


    def delete(self):
        self.log('{}'.format(self.interface))
        self.validate_delete_keys()
        if self.interface_object == None:
            self.log('Nothing to do, interface {} does not exist in netbox.'.format(self.interface))
            return
        try:
            self.interface_object.delete()
        except Exception as e:
            self.log('exiting. Unable to delete interface {}.  Error was: {}'.format(self.interface, e))
            exit(1)


    def create(self):
        self.log('device {}, interface {}'.format(self.device, self.interface))
        try:
            self.nb.dcim.interfaces.create(self.args)
        except Exception as e:
            self.log('exiting. Unable to create interface {}.  Error was: {}'.format(self.interface, e))
            exit(1)


    def update(self):
        self.log('device {} interface {}'.format(self.device, self.interface))
        self.args['id'] = self.interface_id
        try:
            self.interface_object.update(self.args)
        except Exception as e:
            self.log('exiting. Unable to update interface {}.  Error was: {}'.format(self.interface, e))
            exit(1)


    def create_or_update(self):
        self.validate_create_update_keys()
        self.generate_create_update_args()
        if self.interface_object == None:
            self.create()
        else:
            self.update()


    @property
    def description(self):
        if 'description' in self.info:
            return self.info['description']
        else:
            return None


    @property
    def device(self):
        if 'device' in self.info:
            return self.info['device']
        else:
            self.log('exiting. Missing required parameter [device].')
            exit(1)


    @property
    def duplex(self):
        if 'duplex' in self.info:
            return self.info['duplex']
        else:
            return None


    @property
    def interface(self):
        if 'interface' in self.info:
            return self.info['interface']
        else:
            self.log('exiting. Missing required parameter [interface].')
            exit(1)


    @property
    def interface_object(self):
        return self.nb.dcim.interfaces.get(
            device=self.device,
            name=self.interface)


    @property
    def interface_enabled(self):
        if 'interface_enabled' in self.info:
            return self.info['interface_enabled']
        else:
            return None


    @property
    def interface_id(self):
        return self.interface_object.id


    @property
    def interface_mode(self):
        if 'interface_mode' in self.info:
            return self.info['interface_mode']
        else:
            return None


    @property
    def interface_type(self):
        if 'interface_type' in self.info:
            return self.info['interface_type']
        else:
            return None


    @property
    def label(self):
        if 'label' in self.info:
            return self.info['label']
        else:
            return None


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


    @property
    def mtu(self):
        if 'mtu' in self.info:
            return self.info['mtu']
        else:
            return None


    @property
    def untagged_vlan(self):
        if 'untagged_vlan' in self.info:
            return self.info['untagged_vlan']
        else:
            return None
