"""
Name: virtual_ip_address.py
Description: create, update, and delete operations on netbox ip_addresss for virtual machines
"""
from inspect import stack
import sys
from netbox_tools.common import get_vm, vm_id, tag_id
from netbox_tools.virtual_machine import make_vm_primary_ip, map_vm_primary_ip

OUR_VERSION = 105


class VirtualIpAddress:
    """
    create, update, and delete operations on netbox ip_addresss for virtual machines
    netbox_obj = netbox instance
    info = dictionary with the following keys:
        mandatory
            virtual_machine: vm to which the interface belongs e.g. netbox_vm
            interface: interface on which ip addresses will be assigned e.g. vmnet0, etc
            ip4: ipv4 address for the interface e.g. 1.1.1.0/24
        optional
            description: free-form description of the ip address
            role: role of the ip address. Example values: loopback, vip
            status: status of the ip address. Example values: active, reserved, deprecated
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_keys_create_update = set()
        self._mandatory_keys_create_update.add("interface")
        self._mandatory_keys_create_update.add("ip4")
        self._mandatory_keys_create_update.add("virtual_machine")
        self._mandatory_keys_delete = set()
        self._mandatory_keys_delete.add("ip4")
        self._optional_keys = set()
        self._optional_keys.add("description")
        self._optional_keys.add("role")
        self._optional_keys.add("status")
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

    def _validate_keys_create_update(self):
        """
        Verify that all mandatory create/update operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_keys_create_update:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _validate_keys_delete(self):
        """
        Verify that all mandatory delete operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_keys_delete:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_address(self):
        """
        Add address to args
        """
        self._args["address"] = self.ip4

    def _set_assigned_object_id(self):
        """
        Add assigned_object_id to args
        """
        self._args["assigned_object_id"] = vm_id(self._netbox_obj, self.virtual_machine)

    def _set_description(self):
        """
        Add description to args.
        If user has not set this, set a generic description for them.
        """
        if self.description is None:
            self._args["description"] = f"{self.virtual_machine} : {self.ip4}"
        else:
            self._args["description"] = self.description

    def _set_interface(self):
        """
        Add interface to args; converting it to a netbox id
        """
        self._args["interface"] = vm_id(self._netbox_obj, self.virtual_machine)

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

    def _generate_args(self):
        """
        Generate all supported arguments for create and update methods
        """
        self._set_address()
        self._set_assigned_object_id()
        self._set_description()
        self._set_interface()
        self._set_role()
        self._set_status()
        self._set_tags()

    def _initialize_vm_primary_ip(self):
        """
        Initialize primary_ip4 and primary_ip to avoid errors in map_vm_primary_ip()address.save()
        """
        vm_obj = get_vm(self._netbox_obj, self.virtual_machine)
        vm_obj.primary_ip4 = None
        vm_obj.primary_ip = None
        vm_obj.save()

    def create(self):
        """
        create a virtual ip address
        """
        self.log(f"virtual_machine {self.virtual_machine}, address {self.ip4}")
        try:
            self._netbox_obj.ipam.ip_addresses.create(self._args)
        except Exception as _general_exception:
            self.log(
                "exiting.",
                f"Unable to create virtual_machine {self.virtual_machine} ip_address {self.ip4}."
                f"Exception detail {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update a virtual ip address
        """
        self.log(f"virtual_machine {self.virtual_machine}, address {self.ip4}")
        self._args["id"] = self.ip_address_id
        try:
            self.ip_address_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                "exiting.",
                f"Unable to update virtual_machine {self.virtual_machine} ip_address {self.ip4}."
                f"Exception detail {_general_exception}",
            )
            sys.exit(1)

    def delete(self):
        """
        delete a virtual ip address
        """
        self._validate_keys_delete()
        if self.ip_address_obj is None:
            self.log("Nothing to do.", f"ip_address {self.ip4} not found in Netbox.")
            return
        self.log(f"address {self.ip4}")
        try:
            self.ip_address_obj.delete()
        except Exception as _general_exception:
            self.log(
                "exiting.",
                f"Unable to delete ip_address {self.ip4}."
                f"Exception detail {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_keys_create_update()
        self._generate_args()
        self._initialize_vm_primary_ip()
        if self.ip_address_obj is None:
            self.create()
        else:
            self.update()
        map_vm_primary_ip(
            self._netbox_obj, self.virtual_machine, self.interface, self.ip4
        )
        make_vm_primary_ip(self._netbox_obj, self.virtual_machine, self.ip4)

    @property
    def description(self):
        """
        Return the ip description set by the caller.
        Return None if the caller did not set this.
        """
        if "description" in self._info:
            return self._info["description"]
        return None

    @property
    def status(self):
        """
        Return the ip status set by the caller.
        Return None if the caller did not set this.
        """
        if "status" in self._info:
            return self._info["status"]
        return None

    @property
    def ip_address_obj(self):
        """
        Return the Netbox ip address object associated with ip4 address set by the caller.
        """
        try:
            address, mask = self.ip4.split("/")
        except Exception as _general_exception:
            self.log(
                "exiting. Unexpected IP address format.  Expected A.B.C.D/E.",
                f"Got {self.ip4}." f"Exception detail: {_general_exception}",
            )
            sys.exit(1)
        return self._netbox_obj.ipam.ip_addresses.get(address=address, mask=mask)

    @property
    def ip_address_enabled(self):
        """
        Return the enabled status set by the caller.
        Return None if the caller did not set this.
        """
        if "ip_address_enabled" in self._info:
            return self._info["ip_address_enabled"]
        return None

    @property
    def ip_address_id(self):
        """
        Return the Netbox ID for the ip4 address set by the caller.
        """
        return self.ip_address_obj.id

    @property
    def ip_address_type(self):
        """
        Return the ip address type set by the caller.
        Return None if the caller did not set this.
        """
        if "ip_address_type" in self._info:
            return self._info["ip_address_type"]
        return None

    @property
    def interface(self):
        """
        Return the interface set by the caller.
        """
        return self._info["interface"]

    @property
    def ip4(self):
        """
        Return the ipv4 address set by the caller.
        """
        return self._info["ip4"]

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
    def tags(self):
        """
        Return the list of tag names set by the caller.
        If the caller didn't set this, return None.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None

    @property
    def virtual_machine(self):
        """
        Return the virtual machine set by the caller.
        """
        return self._info["virtual_machine"]
