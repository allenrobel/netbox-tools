"""
Name: interface.py
Description: Create, update, delete operations on netbox interfaces
"""
from inspect import stack
import sys
from netbox_tools.common import device_id, netbox_id_untagged_vlan

OUR_VERSION = 104


class Interface:
    """
    create, update, and delete operations on netbox dcim.interfaces
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_create_update_keys = ["interface", "device"]
        self._mandatory_delete_keys = ["interface", "device"]
        # optional_keys is just FYI.  It's not used anywhere.
        self._optional_keys = set()
        self._optional_keys.add("description")
        self._optional_keys.add("duplex")  # str - half, full, auto
        self._optional_keys.add("interface_enabled")  # bool - is the interface enabled
        self._optional_keys.add("interface_mode")  # str - access, tagged, tagged-all
        self._optional_keys.add("interface_type")  # str - interface PHY type
        self._optional_keys.add("label")  # str - physical label
        self._optional_keys.add("mac_address")  # str - interface mac address
        self._optional_keys.add("mgmt_only")  # bool - interface management only flag
        self._optional_keys.add("mtu")  # int - the interface maximum transfer unit
        self._optional_keys.add("untagged_vlan")  # int - interface untagged vlan value
        self._default_interface_type = "1000base-t"
        self._default_interface_mode = "access"
        self._default_interface_enabled = True
        self._default_mgmt_only = False
        self._fix_deprecations()
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
        retrieve valid interface choices from the users netbox instance
        """
        self.valid_choices = {}
        choices_dict = self._netbox_obj.dcim.interfaces.choices()
        for item in choices_dict:
            valid_values = choices_dict[item]
            self.valid_choices[item] = [item["value"] for item in valid_values]

    def _fix_deprecations(self):
        """
        We changed some key names for devices on 2022-09-29.
        If the caller presents the old key names, warn them and convert
        them to the new key names.
        TODO: remove this method on 2023-09-29
        """
        if "mgmt_interface" in self._info:
            self.log(
                "WARNING: devices: <device>: mgmt_interface in your YAML file is deprecated.",
                "Use devices: <device>: interface instead.",
            )
            self._info["interface"] = self._info["mgmt_interface"]
        if "name" in self._info:
            self.log(
                "WARNING: devices: <device>: name in your YAML file is deprecated.",
                "Use devices: <device>: device instead.",
            )
            self._info["device"] = self._info["name"]

    def _validate_delete_keys(self):
        """
        Verify that all mandatory delete operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_delete_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _validate_create_update_keys(self):
        """
        Verify that all mandatory create/update operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_create_update_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_description(self):
        """
        Update args with interface description if the user has set this.
        """
        if self.description is not None:
            self._args["description"] = self.description

    def _set_device(self):
        """
        Update args with the device ID.
        If the device does not exist in netbox, exit with an error.
        """
        self._args["device"] = device_id(self._netbox_obj, self.device)
        if self._args["device"] is None:
            self.log(f"exiting. Device {self.device} does not exist in netbox")
            sys.exit(1)

    def _set_duplex(self):
        """
        Update args with interface duplex if the user has set this.
        If the device does not exist in netbox, exit with an error.
        """
        if self.duplex is None:
            return
        if self.duplex in self.valid_choices["duplex"]:
            self._args["duplex"] = self.duplex
        else:
            _valid_choices = ",".join(sorted(self.valid_choices["duplex"]))
            self.log(
                f"exiting. Invalid duplex. Got {self.duplex}",
                f"Expected one of {_valid_choices}.",
            )
            sys.exit(1)

    def _set_interface_enabled(self):
        """
        Update args with interface enabled, if the user has set this.
        If the user hasn't set this, update args with the default setting.
        If the user set this, but used an invalid (non-boolean) value, exit with an error.
        """
        if isinstance(self.interface_enabled, bool):
            self._args["enabled"] = self.interface_enabled
        elif self.interface_enabled is None:
            self._args["enabled"] = self._default_interface_enabled
        else:
            self.log(
                f"exiting. Invalid value for interface_enabled. Got {self.interface_enabled}.",
                "Expected boolean.",
            )
            sys.exit(1)

    def _set_interface_mode(self):
        """
        Update args with interface mode, if the user has set this.
        If the user set this, but used an invalid value, exit with an error.
        """
        if self.interface_mode is None:
            return
        if self.interface_mode in self.valid_choices["mode"]:
            self._args["mode"] = self.interface_mode
        else:
            _valid_choices = ",".join(sorted(self.valid_choices["mode"]))
            self.log(
                f"exiting. Invalid interface_mode. Got {self.interface_mode}.",
                f"Expected one of {_valid_choices}.",
            )
            sys.exit(1)

    def _set_interface_type(self):
        """
        Update args with interface type, if the user has set this.
        If the user set this, but used an invalid value, exit with an error.
        """
        if self.interface_type is None:
            self.log("exiting. missing required argument: interface_type")
            sys.exit(1)
        if self.interface_type in self.valid_choices["type"]:
            self._args["type"] = self.interface_type
        else:
            _valid_choices = ",".join(sorted(self.valid_choices["type"]))
            self.log(
                f"exiting. Invalid interface_type. Got {self.interface_type}.",
                f"Expected one of {_valid_choices}.",
            )
            sys.exit(1)

    def _set_label(self):
        """
        Update args with the physical interface label, if the user has set this.
        """
        if self.label is not None:
            self._args["label"] = self.label

    def _set_mac_address(self):
        """
        Update args with the interface mac address, if the user has set this.
        """
        if self.mac_address is not None:
            self._args["mac_address"] = self.mac_address

    def _set_mgmt_only(self):
        """
        Update args with the interface mgmt_only flag, if the user has set this.
        If the user has not set this, apply the default mgmt_only flag value.
        If the user set this, but used an invalid (non-boolean) value, exit with an error.
        """
        if isinstance(self.mgmt_only, bool):
            self._args["mgmt_only"] = self.mgmt_only
        elif self.mgmt_only is None:
            self._args["mgmt_only"] = self._default_mgmt_only
        else:
            self.log(
                f"exiting. Invalid value for mgmt_only. Got {self.mgmt_only}",
                "Expected boolean.",
            )
            sys.exit(1)

    def _set_mtu(self):
        """
        Update args with the interface maximum transfer unit, if the user has set this.
        """
        if self.mtu is not None:
            self._args["mtu"] = self.mtu

    def _set_untagged_vlan(self):
        """
        Update args with the interface untagged vlan, if the user has set this.
        """
        if self.untagged_vlan is not None:
            self._args["untagged_vlan"] = netbox_id_untagged_vlan(
                self._netbox_obj, self.untagged_vlan
            )

    def _generate_create_update_args(self):
        """
        Generate all supported arguments for create and update methods
        """
        self._args["name"] = self.interface
        self._set_description()
        self._set_device()
        self._set_duplex()
        self._set_interface_enabled()
        self._set_interface_mode()
        self._set_interface_type()
        self._set_label()
        self._set_mac_address()
        self._set_mgmt_only()
        self._set_mtu()
        self._set_untagged_vlan()

    def delete(self):
        """
        Delete an interface, if it exists in netbox.
        """
        self.log(f"{self.interface}")
        self._validate_delete_keys()
        if self.interface_object is None:
            self.log(
                f"Nothing to do, interface {self.interface} does not exist in netbox."
            )
            return
        try:
            self.interface_object.delete()
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to delete interface {self.interface}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create(self):
        """
        Create an interface.
        """
        self.log(f"device {self.device}, interface {self.interface}")
        try:
            self._netbox_obj.dcim.interfaces.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to create interface {self.interface}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        Update an interface.
        """
        self.log(f"device {self.device} interface {self.interface}")
        self._args["id"] = self.interface_id
        try:
            self.interface_object.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to update interface {self.interface}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        Entry point into create and update methods
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
        Return the interface description set by the caller.
        If the caller didn't set this, return None.
        """
        if "description" in self._info:
            return self._info["description"]
        return None

    @property
    def device(self):
        """
        Return the device associated with the interface set by the caller.
        If the caller didn't set this mandatory parameter, exit with an error.
        """
        if "device" in self._info:
            return self._info["device"]
        self.log("exiting. Missing required parameter [device].")
        sys.exit(1)

    @property
    def duplex(self):
        """
        Return the interface duplex set by the caller.
        If the caller didn't set this, return None.
        """
        if "duplex" in self._info:
            return self._info["duplex"]
        return None

    @property
    def interface(self):
        """
        Return the interface set by the caller.
        If the caller didn't set this mandatory parameter, exit with an error.
        """
        if "interface" in self._info:
            return self._info["interface"]
        self.log("exiting. Missing required parameter [interface].")
        sys.exit(1)

    @property
    def interface_object(self):
        """
        Return the netbox interface object associated with the
        device and interface parameters set by the caller.
        If the caller didn't set either device or interface, these
        properties will exit with an error, so no need here for
        error handling.
        """
        return self._netbox_obj.dcim.interfaces.get(
            device=self.device, name=self.interface
        )

    @property
    def interface_enabled(self):
        """
        Return the interface enabled value set by the caller.
        If the caller didn't set this, return None.
        """
        if "interface_enabled" in self._info:
            return self._info["interface_enabled"]
        return None

    @property
    def interface_id(self):
        """
        Return the netbox interface object ID.
        No error handling is needed here since appropriate handling is already performed
        in the device and interface properties.
        """
        return self.interface_object.id

    @property
    def interface_mode(self):
        """
        Return the interface mode set by the caller.
        If the caller didn't set this, return None.
        """
        if "interface_mode" in self._info:
            return self._info["interface_mode"]
        return None

    @property
    def interface_type(self):
        """
        Return the interface type set by the caller.
        If the caller didn't set this, return None.
        """
        if "interface_type" in self._info:
            return self._info["interface_type"]
        return None

    @property
    def label(self):
        """
        Return the interface physical label set by the caller.
        If the caller didn't set this, return None.
        """
        if "label" in self._info:
            return self._info["label"]
        return None

    @property
    def mac_address(self):
        """
        Return the interface mac address set by the caller.
        If the caller didn't set this, return None.
        """
        if "mac_address" in self._info:
            return self._info["mac_address"]
        return None

    @property
    def mgmt_only(self):
        """
        Return the interface mgmt_only flag value set by the caller.
        If the caller didn't set this, return None.
        """
        if "mgmt_only" in self._info:
            return self._info["mgmt_only"]
        return None

    @property
    def mtu(self):
        """
        Return the interface maximum transfer unit set by the caller.
        If the caller didn't set this, return None.
        """
        if "mtu" in self._info:
            return self._info["mtu"]
        return None

    @property
    def untagged_vlan(self):
        """
        Return the interface untagged vlan value set by the caller.
        If the caller didn't set this, return None.
        """
        if "untagged_vlan" in self._info:
            return self._info["untagged_vlan"]
        return None
