"""
Name: ip_address.py
Description: create, update and delete operations on netbox ip_address

NOTES:

1. For create and update operations, this class also maps and assigns the
IP address as a device's primary IP.  We shouldn't have to do this, but
are seeing Netbox get into a state where the IPAM -> IP Addresses
page will not load if the IP address is not mapped to a device.
"""
from inspect import stack
import sys
from netbox_tools.common import device_id
from netbox_tools.device import (
    map_device_primary_ip,
    make_device_primary_ip,
    initialize_device_primary_ip,
)

OUR_VERSION = 103

class IpAddress:
    """
    create, update, delete operations on Netbox ipam.ip_address

    Parameters:
        netbox_obj = netbox instance
        info = dictionary with the following keys:

        # mandatory
        device: device to which the interface belongs e.g. cvd_leaf_1
        interface: interface on which ip addresses will be assigned: mgmt0, Eth1/1, Vlan150, etc
        ip4: ipv4 address for the interface e.g. 1.1.1.0/24
        # optional
        description: free-form description of the ip address
        status: ip address status.
        role: ip address role.
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_create_update_keys = set()
        self._mandatory_create_update_keys.add("interface")
        self._mandatory_create_update_keys.add("ip4")
        self._mandatory_create_update_keys.add("device")

        self._mandatory_delete_keys = set()
        self._mandatory_delete_keys.add("ip4")

        self._optional_keys = set()
        self._optional_keys.add("description")
        self._optional_keys.add("role")
        self._optional_keys.add("status")
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
        retrieve valid ip address choices from the users netbox instance
        """
        self._valid_choices = {}
        choices_dict = self._netbox_obj.ipam.ip_addresses.choices()
        for item in choices_dict:
            valid_values = choices_dict[item]
            self._valid_choices[item] = [item["value"] for item in valid_values]

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

    def _set_address(self):
        self._args["address"] = self.ip4

    def _set_assigned_object_id(self):
        self._args["assigned_object_id"] = device_id(self._netbox_obj, self.device)

    def _set_description(self):
        """
        Update args with description, if the user has set this.
        If the user has not set this, update args with a generic description
        which includes device, interface, and ip4 address
        """
        if self.description is not None:
            self._args["description"] = self.description
        else:
            self._args["description"] = f"{self.device} : {self.interface} : {self.ip4}"

    def _set_role(self):
        """
        Update args with the ip address role, if the user has set this.
        Exit with error if the user set an invalid role.
        """
        if self.role is None:
            return
        if self.role in self._valid_choices["role"] or self.role == "":
            self._args["role"] = self.role
        else:
            _valid_choices = ",".join(sorted(self._valid_choices["role"]))
            self.log(
                f"exiting. Invalid role. Got {self.role}",
                f"Expected one of {_valid_choices}.",
            )
            sys.exit(1)

    def _set_status(self):
        """
        Update args with the ip address status, if the user has set this.
        Exit with error if the user set an invalid status.
        """
        if self.status is None:
            return
        if self.status in self._valid_choices["status"]:
            self._args["status"] = self.status
        else:
            _valid_choices = ",".join(sorted(self._valid_choices["status"]))
            self.log(
                f"exiting. Invalid status. Got {self.status}",
                f"Expected one of {_valid_choices}.",
            )
            sys.exit(1)

    def _set_tags(self):
        """
        Add tags, if any, to args; converting them to netbox IDs
        """
        if self.tags is None:
            return
        self._args["tags"] = []
        for tag in self.tags:
            tid = tag_id(self._netbox_obj, tag)
            if tid is None:
                self.log(f"tag {tag} not found in Netbox.  Skipping.")
                continue
            self._args["tags"].append(tid)

    def _generate_create_update_args(self):
        """
        Generate all supported arguments for create and update methods
        """
        self._set_address()
        self._set_assigned_object_id()
        self._set_description()
        self._set_role()
        self._set_status()
        self._set_tags()

    def delete(self):
        """
        Delete an ip address.
        """
        self._validate_delete_keys()
        if self.ip_address_obj is None:
            self.log(f"Nothing to do. IP address {self.ip4} does not exist in netbox.")
            return
        self.log(f"{self.ip4}")
        try:
            self.ip_address_obj.delete()
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to delete ip_address {self.ip4}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create(self):
        """
        Create an ip address.
        """
        self.log(f"device {self.device} address {self.ip4}")
        try:
            self._netbox_obj.ipam.ip_addresses.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to create device {self.device} ip_address {self.ip4}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        Update an ip address.
        """
        self.log(f"device {self.device} address {self.ip4}")
        self._args["id"] = self.ip_address_id
        try:
            self.ip_address_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to update device {self.device} ip_address {self.ip4}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        Entry point into create and update methods
        """
        self._validate_create_update_keys()
        self._generate_create_update_args()
        initialize_device_primary_ip(self._netbox_obj, self.device)
        if self.ip_address_obj is None:
            self.create()
        else:
            self.update()
        map_device_primary_ip(self._netbox_obj, self.device, self.interface, self.ip4)
        make_device_primary_ip(self._netbox_obj, self.device, self.ip4)

    @property
    def description(self):
        """
        Return the ip address description set by the caller.
        If the caller didn't set this, return None.
        """
        if "description" in self._info:
            return self._info["description"]
        return None

    @property
    def device(self):
        """
        Return the device set by the caller.
        We've already checked that this is set in _validate_create_update_keys()
        """
        return self._info["device"]

    @property
    def interface(self):
        """
        Return the interface set by the caller.
        We've already checked that this is set in _validate_create_update_keys()
        """
        return self._info["interface"]

    @property
    def ip_address_obj(self):
        """
        Return the ip address object associated with the ip address and mask set by the caller.
        """
        try:
            address, mask = self.ip4.split("/")
        except Exception as _general_exception:
            self.log(
                "IpAddress: exiting. Unexpected IP address format.  Expected A.B.C.D/E.",
                f"Got {self.ip4}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)
        return self._netbox_obj.ipam.ip_addresses.get(address=address, mask=mask)

    @property
    def ip_address_id(self):
        """
        Return the Netbox ID associated with the ip address object.
        If the ip address object doesn't exist, None will be returned.
        """
        return self.ip_address_obj.id

    @property
    def ip4(self):
        """
        Return the ipv4 address set by the caller.
        We've already checked that this is set in _validate_create_update_keys()
        """
        return self._info["ip4"]

    @property
    def mgmt_interface(self):
        """
        Keeping for backward-compatibility.
        TODO: Remove after 2023-09-29
        """
        return self._info["interface"]

    @property
    def role(self):
        """
        Return the ip address role set by the caller.
        If the caller didn't set this, return None
        """
        if "role" in self._info:
            return self._info["role"]
        return None

    @property
    def status(self):
        """
        Return the ip address status set by the caller.
        If the caller didn't set this, return None.
        """
        if "status" in self._info:
            return self._info["status"]
        return None

    @property
    def tags(self):
        """
        Return the list of tag names set by the caller.
        If the caller didn't set this, return None.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
