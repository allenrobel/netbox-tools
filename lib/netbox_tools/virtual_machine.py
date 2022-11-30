"""
Name: virtual_machine.py
Description: create/update/delete operations on netbox virtual_machine
"""
from inspect import stack, getframeinfo, currentframe
import sys
from netbox_tools.common import cluster_id
from netbox_tools.common import create_slug
from netbox_tools.common import device_id
from netbox_tools.common import get_vm
from netbox_tools.common import ip_address_id, get_ip_address
from netbox_tools.common import role_id
from netbox_tools.common import site_id
from netbox_tools.common import tag_id
from netbox_tools.common import virtual_interface_id

OUR_VERSION = 105


class VirtualMachine:
    """
    create/update/delete operations on netbox virtual_machine
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_keys_create_or_update = ["vm", "role"]
        self._mandatory_keys_delete = ["vm"]

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _validate_keys_delete(self):
        for key in self._mandatory_keys_delete:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _validate_keys_create_or_update(self):
        for key in self._mandatory_keys_create_or_update:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_cluster(self):
        """
        Add cluster, if any, to args
        """
        if self.cluster is not None:
            self._args["cluster"] = cluster_id(self._netbox_obj, self.cluster)

    def _set_comments(self):
        """
        Add comments, if any, to args
        """
        if self.comments is not None:
            self._args["comments"] = self.comments

    def _set_device(self):
        """
        Add device, if any, to args
        """
        if self.device is not None:
            self._args["device"] = device_id(self._netbox_obj, self.device)

    def _set_disk(self):
        """
        Add disk, if any, to args
        """
        if self.disk is not None:
            self._args["disk"] = self.disk

    def _set_memory(self):
        """
        Add memory, if any, to args
        """
        if self.memory is not None:
            self._args["memory"] = self.memory

    def _set_name(self):
        """
        Add name to args
        """
        self._args["name"] = self.vm_name

    def _set_role(self):
        """
        Add role, if any, to args; converting to its corresponding netbox id
        """
        if self.role is not None:
            self._args["role"] = role_id(self._netbox_obj, self.role)

    def _set_site(self):
        """
        Add site, if any, to args; converting to its corresponding netbox id
        """
        if self.site is not None:
            self._args["site"] = site_id(self._netbox_obj, self.site)

    def _set_slug(self):
        """
        Add slug to args
        """
        self._args["slug"] = create_slug(self._info["vm"])

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

    def _set_vcpus(self):
        """
        Add vcpus, if any, to args
        (float) virtual cpu units allocated to the vm. Min value: 0.01
        """
        if self.vcpus is None:
            return
        try:
            vcpus = float(str(self.vcpus))
        except ValueError as _value_error:
            self.log(
                "exiting. vcpus must be of type float. e.g. 1.01.", f"Got {self.vcpus}"
            )
            sys.exit(1)
        if vcpus < 0.01:
            self.log("exiting. vcpus must be greater than 0.01.", f"Got {vcpus}")
            sys.exit(1)
        self._args["vcpus"] = vcpus

    def _generate_args_create_or_update(self):
        """
        generate all supported arguments for create/update operations
        """
        self._set_comments()
        self._set_cluster()
        self._set_device()
        self._set_disk()
        self._set_memory()
        self._set_name()
        self._set_role()
        self._set_site()
        self._set_slug()
        self._set_tags()
        self._set_vcpus()

    def create(self):
        """
        create a virtual machine
        """
        self.log(f"{self.vm_name}")
        try:
            self._netbox_obj.virtualization.virtual_machines.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to create vm {self.vm_name}."
                f"Exception detail: {_general_exception}"
            )
            sys.exit(1)

    def update(self):
        """
        update a virtual machine
        """
        self.log(f"{self.vm_name}")
        self._args["id"] = self.vm_id
        try:
            self.vm_object.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to update vm {self.vm_name}."
                f"Exception detail: {_general_exception}"
            )
            sys.exit(1)

    def delete(self):
        """
        delete a virtual machine
        """
        self.log(f"{self.vm_name}")
        self._validate_keys_delete()
        if self.vm_object is None:
            self.log(f"Nothing to do, vm {self.vm_name} does not exist in netbox.")
            return
        try:
            self.vm_object.delete()
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to delete vm {self.vm_name}."
                f"Exception detail: {_general_exception}"
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into creation and updation methods
        """
        self._validate_keys_create_or_update()
        self._generate_args_create_or_update()
        if self.vm_object is None:
            self.create()
        else:
            self.update()

    @property
    def cluster(self):
        """
        Return the cluster set by the caller.
        If the caller didn't set this, return None.
        """
        if "cluster" in self._info:
            return self._info["cluster"]
        return None

    @property
    def comments(self):
        """
        Return the comments set by the caller.
        If the caller didn't set this, return None.
        """
        if "comments" in self._info:
            return self._info["comments"]
        return None

    @property
    def device(self):
        """
        Return the device set by the caller.
        If the caller didn't set this, return None.

        The device hosting the virtual machine. device must already exist in netbox.
        If device is defined, cluster must also be defined.  We don't test for that
        here since netbox returns a good error message.
        """
        if "device" in self._info:
            return self._info["device"]
        return None

    @property
    def disk(self):
        """
        Return the disk space set by the caller.
        If the caller didn't set this, return None.

        (int) disk space allocated to the vm, in GB
        """
        if "disk" in self._info:
            return self._info["disk"]
        return None

    @property
    def memory(self):
        """
        Return the memory set by the caller.
        If the caller didn't set this, return None.

        (int) memory allocated to the vm, in MB
        """
        if "memory" in self._info:
            return self._info["memory"]
        return None

    @property
    def role(self):
        """
        Return the role set by the caller.
        If the caller didn't set this, return None.

        (str) role the vm serves. role must already exist in netbox
        """
        if "role" in self._info:
            return self._info["role"]
        return None

    @property
    def site(self):
        """
        Return the site set by the caller.
        If the caller didn't set this, return None.

        site in which the vm is located. site must already exist in netbox
        """
        if "site" in self._info:
            return self._info["site"]
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
    def vcpus(self):
        """
        Return the vcpus set by the caller.
        If the caller didn't set this, return None.

        (float) virtual cpu units allocated to the vm. Min value: 0.01
        """
        if "vcpus" in self._info:
            return self._info["vcpus"]
        return None

    @property
    def vm_name(self):
        """
        Return the virtual machine name set by the caller.
        """
        return self._info["vm"]

    @property
    def vm_id(self):
        """
        Return the netbox ID of the virtual machine.
        """
        return self.vm_object.id

    @property
    def vm_object(self):
        """
        Return the netbox object associated with the virtual machine.
        """
        try:
            return self._netbox_obj.virtualization.virtual_machines.get(
                name=self.vm_name
            )
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to retrieve vm_object associated with {self.vm_name}",
                f"Exceptioin detail: {_general_exception}",
            )
            sys.exit(1)


# utility functions related to virtual machines


def initialize_vm_primary_ip(netbox_obj, vm_name):
    """
    Initialize primary_ip4 and primary_ip to avoid errors in map_vm_primary_ip()address.save()
    """
    vm_obj = get_vm(netbox_obj, vm_name)
    vm_obj.primary_ip4 = None
    vm_obj.primary_ip = None
    vm_obj.save()
    print(
        "{}(v{}).{}: vm: {}".format(
            __name__, OUR_VERSION, getframeinfo(currentframe()).function, vm_name
        )
    )


def map_vm_primary_ip(netbox_obj, vm_name, interface_name, ip_address):
    """
    Map an existing IP address to an interface ID

    args: nb, vm_name, interface_name, ip_address

    Where:

        netbox_obj - netbox instance

        vm_name - str() name of a virtual machine

        interface_name - str() name of an interface

        ip_address - str() ip address in A.B.C.D/E format
    """
    address = get_ip_address(netbox_obj, ip_address)
    address.assigned_object_id = virtual_interface_id(
        netbox_obj, vm_name, interface_name
    )
    address.assigned_object_type = "virtualization.vminterface"
    address.save()
    print(
        "{}(v{}).{}: vm: {}, interface: {}, address: {}".format(
            __name__,
            OUR_VERSION,
            getframeinfo(currentframe()).function,
            vm_name,
            interface_name,
            ip_address,
        )
    )


def make_vm_primary_ip(netbox_obj, vm_name, ip_address):
    """
    Make an ip address the primary address for a virtual_machine by mapping
    the address ID to a virtual_machines's primary_ip and primary_ip4.
    """
    vm_obj = get_vm(netbox_obj, vm_name)
    address_id = ip_address_id(netbox_obj, ip_address)
    vm_obj.primary_ip = address_id
    vm_obj.primary_ip4 = address_id
    vm_obj.save()
    print(
        "{}(v{}).{}: vm: {}, ip: {}".format(
            __name__,
            OUR_VERSION,
            getframeinfo(currentframe()).function,
            vm_name,
            ip_address,
        )
    )
