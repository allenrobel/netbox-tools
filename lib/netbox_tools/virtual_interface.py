'''
Name: virtual_interface.py
Description: Create, update, delete operations on netbox virtual_interfaces
'''

from netbox_tools.common import vm_id, netbox_id_untagged_vlan

class VirtualInterface(object):
    def __init__(self, nb, info):
        self.version = 100
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_create_update_keys = ['interface', 'virtual_machine']
        self.mandatory_delete_keys = ['interface', 'virtual_machine']
        # optional_keys is just FYI.  It's not referenced anywhere.
        self.optional_keys = set()
        self.optional_keys.add('description')
        self.optional_keys.add('interface_enabled')   # bool - is the interface enabled
        self.optional_keys.add('interface_mode')      # str - access, tagged, tagged-all
        self.optional_keys.add('mac_address')         # str - interface mac address
        self.optional_keys.add('mtu')
        self.optional_keys.add('untagged_vlan')
        self.default_interface_mode = 'access'
        self.default_interface_enabled = True
        self.populate_valid_choices()


    def populate_valid_choices(self):
        self.valid_choices = dict()
        choices_dict = self.nb.virtualization.interfaces.choices()
        for item in choices_dict:
            valid_values = choices_dict[item]
            self.valid_choices[item] = [item['value'] for item in valid_values]


    def validate_delete_keys(self):
        for key in self.mandatory_delete_keys:
            if key not in self.info:
                print('VirtualInterface.validate_delete_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)


    def validate_create_update_keys(self):
        for key in self.mandatory_create_update_keys:
            if key not in self.info:
                print('VirtualInterface.validate_create_update_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)


    def set_description(self):
        if self.description != None:
            self.args['description'] = self.description


    def set_interface_enabled(self):
        if isinstance(self.interface_enabled, bool):
            self.args['enabled'] = self.interface_enabled
        elif self.interface_enabled == None:
            self.args['enabled'] = self.default_interface_enabled
        else:
            print('VirtualInterface.set_interface_enabled: exiting. Invalid value for interface_enabled. Got {}. Expected boolean.'.format(
                self.interface_enabled))
            exit(1)


    def set_interface_mode(self):
        if self.interface_mode == None:
            return
        if self.interface_mode in self.valid_choices['mode']:
            self.args['mode'] = self.interface_mode
        else:
            print('VirtualInterface.set_interface_mode: exiting. Invalid interface_mode. Got {}. Expected one of {}.'.format(
                self.interface_mode,
                ','.join(sorted(self.valid_choices['mode']))))
            exit(1)


    def set_mac_address(self):
        if self.mac_address != None:
            self.args['mac_address'] = self.mac_address


    def set_mtu(self):
        if self.mtu != None:
            self.args['mtu'] = self.mtu


    def set_name(self):
        self.args['name'] = self.interface


    def set_untagged_vlan(self):
        if self.untagged_vlan != None:
            self.args['untagged_vlan'] = netbox_id_untagged_vlan(self.nb, self.untagged_vlan)


    def set_virtual_machine(self):
        self.args['virtual_machine'] = vm_id(self.nb, self.virtual_machine)


    def generate_create_update_args(self):
        self.set_description()
        self.set_interface_enabled()
        self.set_interface_mode()
        self.set_mac_address()
        self.set_mtu()
        self.set_name()
        self.set_untagged_vlan()
        self.set_virtual_machine()


    def delete(self):
        print('VirtualInterface.delete: {}'.format(self.interface))
        self.validate_delete_keys()
        if self.interface_object == None:
            print('VirtualInterface.delete: Nothing to do, interface {} does not exist in netbox.'.format(self.interface))
            return
        try:
            self.interface_object.delete()
        except Exception as e:
            print('VirtualInterface.delete: Exiting. Unable to delete interface {}.  Error was: {}'.format(self.interface, e))
            exit(1)


    def create(self):
        print('VirtualInterface.create: {} {}'.format(self.virtual_machine, self.interface))
        try:
            self.nb.virtualization.interfaces.create(self.args)
        except Exception as e:
            print('VirtualInterface.create: exiting. Unable to create interface {}.  Error was: {}'.format(self.interface, e))
            exit(1)


    def update(self):
        print('VirtualInterface.update: {} {}'.format(self.virtual_machine, self.interface))
        self.args['id'] = self.interface_id
        try:
            self.interface_object.update(self.args)
        except Exception as e:
            print('VirtualInterface.update: Exiting. Unable to update virtual_machine {} interface {}.  Error was: {}'.format(
                self.virtual_machine,
                self.interface,
                e))
            exit(1)


    def create_or_update(self):
        self.validate_create_update_keys()
        self.generate_create_update_args()
        print('HERE1: self.interface_object {}'.format(self.interface_object))
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
    def interface(self):
        if 'interface' in self.info:
            return self.info['interface']
        else:
            print('VirtualInterface.interface: exiting. Missing required parameter [interface].')
            exit(1)


    @property
    def interface_object(self):
        return self.nb.virtualization.interfaces.get(
            virtual_machine_id=self.vm_id,
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
    def mac_address(self):
        if 'mac_address' in self.info:
            return self.info['mac_address']
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


    @property
    def vm_id(self):
        try:
            vm = self.nb.virtualization.virtual_machines.get(name=self.virtual_machine)
            return vm.id
        except Exception as e:
            print('VirtualInterface.vm_id: returning None. exception was: {}'.format(e))
            return None


    @property
    def virtual_machine(self):
        if 'virtual_machine' in self.info:
            return self.info['virtual_machine']
        else:
            return None
