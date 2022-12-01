'''
Name: virtual_interface.py
Description: create, update, delete operations on netbox virtual_interfaces
'''
from inspect import stack
import sys
from netbox_tools.common import vm_id, netbox_id_untagged_vlan

OUR_VERSION = 101
class VirtualInterface():
    """
    create, update, delete operations on netbox virtual_interfaces
    """
    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_create_update_keys = set()
        self._mandatory_create_update_keys.add('interface')
        self._mandatory_create_update_keys.add('virtual_machine')
        self._mandatory_delete_keys = set()
        self._mandatory_delete_keys.add('interface')
        self._mandatory_delete_keys.add('virtual_machine')
        # _optional_keys is just FYI.  It's not used anywhere.
        self._optional_keys = set()
        self._optional_keys.add('description')
        self._optional_keys.add('interface_enabled')   # bool - is the interface enabled
        self._optional_keys.add('interface_mode')      # str - access, tagged, tagged-all
        self._optional_keys.add('mac_address')         # str - interface mac address
        self._optional_keys.add('mtu')
        self._optional_keys.add('untagged_vlan')
        self._default_interface_enabled = True
        self._populate_valid_choices()


    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )


    def _populate_valid_choices(self):
        """
        retrieve valid ip address choices from the users netbox instance
        """
        self.valid_choices = {}
        choices_dict = self._netbox_obj.virtualization.interfaces.choices()
        for item in choices_dict:
            valid_values = choices_dict[item]
            self.valid_choices[item] = [item['value'] for item in valid_values]


    def _validate_delete_keys(self):
        """
        Verify that all mandatory delete operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_delete_keys:
            if key not in self._info:
                self.log(
                    f"exiting. mandatory key {key} not found in info {self._info}"
                )
                sys.exit(1)


    def _validate_create_update_keys(self):
        """
        Verify that all mandatory create/update operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_create_update_keys:
            if key not in self._info:
                self.log(
                    f"exiting. mandatory key {key} not found in info {self._info}"
                )
                sys.exit(1)


    def _set_description(self):
        """
        Add interface description to args, if it is set.
        """
        if self.description is not None:
            self._args['description'] = self.description


    def _set_interface_enabled(self):
        """
        Add interface enabled state to args.
        If user provided non-boolean value, exit with error.
        If user didn't provide a value, set enabled state to True.
        """
        if isinstance(self.interface_enabled, bool):
            self._args['enabled'] = self.interface_enabled
        elif self.interface_enabled is None:
            self._args['enabled'] = self._default_interface_enabled
        else:
            self.log(
                "exiting. Invalid value for interface_enabled.",
                f"Got {self.interface_enabled}. Expected boolean."
            )
            sys.exit(1)


    def _set_interface_mode(self):
        """
        Add interface mode address to args, if it is set.
        If user provided invalid value, exit with error.
        """
        if self.interface_mode is None:
            return
        if self.interface_mode in self.valid_choices['mode']:
            self._args['mode'] = self.interface_mode
        else:
            _valid_choices = ','.join(sorted(self.valid_choices['mode']))
            self.log(
                "exiting. Invalid interface_mode.",
                f"Got {self.interface_mode}. Expected one of {_valid_choices}."
            )
            sys.exit(1)


    def _set_mac_address(self):
        """
        Add interface mac address to args, if it is set.
        """
        if self.mac_address is not None:
            self._args['mac_address'] = self.mac_address


    def _set_mtu(self):
        """
        Add interface mtu to args, if it is set.
        """
        if self.mtu is not None:
            self._args['mtu'] = self.mtu


    def _set_name(self):
        """
        Add interface name to args.
        """
        self._args['name'] = self.interface


    def _set_untagged_vlan(self):
        """
        Add untagged vlan to args, if it is set.
        """
        if self.untagged_vlan is not None:
            self._args['untagged_vlan'] = netbox_id_untagged_vlan(
                self._netbox_obj,
                self.untagged_vlan
            )


    def _set_virtual_machine(self):
        """
        Add virtual machine to args
        """
        self._args['virtual_machine'] = vm_id(self._netbox_obj, self.virtual_machine)


    def _generate_create_update_args(self):
        self._set_description()
        self._set_interface_enabled()
        self._set_interface_mode()
        self._set_mac_address()
        self._set_mtu()
        self._set_name()
        self._set_untagged_vlan()
        self._set_virtual_machine()


    def delete(self):
        """
        delete a virtual machine
        """
        self.log(f"{self.interface}")
        self._validate_delete_keys()
        if self.interface_object is None:
            self.log(f"Nothing to do, interface {self.interface} does not exist in netbox.")
            return
        try:
            self.interface_object.delete()
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to delete interface {self.interface}.",
                f"Exception detail: {_general_exception}"
            )
            sys.exit(1)


    def create(self):
        """
        create a virtual machine
        """
        self.log(f"{self.virtual_machine} {self.interface}")
        try:
            self._netbox_obj.virtualization.interfaces.create(self._args)
        except Exception as _general_exception:
            self.log(
                "Exiting. Unable to create:",
                f"virtual_machine {self.virtual_machine} interface {self.interface}.",
                f"Exception detail: {_general_exception}"
            )
            sys.exit(1)


    def update(self):
        """
        update a virtual machine
        """
        self.log(f"{self.virtual_machine} {self.interface}")
        self._args['id'] = self.interface_id
        try:
            self.interface_object.update(self._args)
        except Exception as _general_exception:
            self.log(
                "Exiting. Unable to update:",
                f"virtual_machine {self.virtual_machine} interface {self.interface}.",
                f"Exception detail: {_general_exception}"
            )
            sys.exit(1)


    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_create_update_keys()
        self._generate_create_update_args()
        if self.interface_object is None:
            self.create()
        else:
            self.update()


    @property
    def description(self):
        """
        Return the description set by the caller.
        Return None if the caller did not set this.
        """
        if 'description' in self._info:
            return self._info['description']
        return None


    @property
    def interface(self):
        """
        Return the interface set by the caller.
        Exit with error if the caller did not set this.
        """
        if 'interface' in self._info:
            return self._info['interface']
        self.log(
            "exiting. Missing required parameter [interface]."
        )
        sys.exit(1)


    @property
    def interface_object(self):
        """
        Return the interface object associated with the
        virtual_machine and interface set by the caller.
        Other properties e.g. vm_id will exit with error
        if the caller did not set requisite parameters.
        """
        return self._netbox_obj.virtualization.interfaces.get(
            virtual_machine_id=self.vm_id,
            name=self.interface)


    @property
    def interface_enabled(self):
        """
        Return the enabled state of the interface set by the caller.
        Return None if the caller did not set this.
        """
        if 'interface_enabled' in self._info:
            return self._info['interface_enabled']
        return None


    @property
    def interface_id(self):
        """
        Return the Netbox interface object ID associated
        with the interface set by the caller.
        Other properties e.g. vm_id will exit with error
        if the caller did not set requisite parameters.
        """
        return self.interface_object.id


    @property
    def interface_mode(self):
        """
        Return the interface mode set by the caller.
        Return None if the caller did not set this.
        """
        if 'interface_mode' in self._info:
            return self._info['interface_mode']
        return None


    @property
    def mac_address(self):
        """
        Return the interface mac address set by the caller.
        Return None if the caller did not set this.
        """
        if 'mac_address' in self._info:
            return self._info['mac_address']
        return None


    @property
    def mtu(self):
        """
        Return the interface maximum transfer unit set by the caller.
        Return None if the caller did not set this.
        """
        if 'mtu' in self._info:
            return self._info['mtu']
        return None


    @property
    def untagged_vlan(self):
        """
        Return the interface untagged vlan set by the caller.
        Return None if the caller did not set this.
        """
        if 'untagged_vlan' in self._info:
            return self._info['untagged_vlan']
        return None


    @property
    def vm_obj(self):
        """
        Return the Netbox object associated with the virtual machine set by the caller.
        Exit with error if this object cannot be retrieved from Netbox.
        """
        try:
            return self._netbox_obj.virtualization.virtual_machines.get(name=self.virtual_machine)
        except Exception as _general_exception:
            self.log(
                "exiting. Unable to retrieve virtual machine object from Netbox",
                f"for virtual_machine name {self.virtual_machine}.",
                f"Exception detail: {_general_exception}"
            )
            sys.exit(1)


    @property
    def vm_id(self):
        """
        Return the Netbox ID of the virtual machine object associated with the
        virtual machine set by the caller.
        If the nv_obj cannot be retrieved from Netbox, the vm_obj property
        will exit with error.
        """
        return self.vm_obj.id


    @property
    def virtual_machine(self):
        """
        Return the virtual machine set by the caller.
        Return None if the caller did not set this.
        """
        if 'virtual_machine' in self._info:
            return self._info['virtual_machine']
        return None
