"""
Name: device.py
Description: Class for create, update, and delete operations on netbox device
"""
from inspect import stack, getframeinfo, currentframe
import sys
from netbox_tools.common import cluster_id
from netbox_tools.common import create_slug
from netbox_tools.common import device_type_id
from netbox_tools.common import get_device
from netbox_tools.common import get_ip_address
from netbox_tools.common import interface_id
from netbox_tools.common import ip_address_id
from netbox_tools.common import location_id
from netbox_tools.common import rack_id
from netbox_tools.common import role_id
from netbox_tools.common import site_id
from netbox_tools.common import tag_id

OUR_VERSION = 104


def initialize_device_primary_ip(netbox_obj, device_name):
    """
    Initialize primary_ip4 and primary_ip to avoid errors in map_device_primary_ip()address.save()
    """
    device = get_device(netbox_obj, device_name)
    device.primary_ip4 = None
    device.primary_ip = None
    device.save()
    func_name = getframeinfo(currentframe()).function
    print(f"{__name__}(v{OUR_VERSION}).{func_name}: device: {device_name}")


def map_device_primary_ip(netbox_obj, device_name, interface_name, ip4):
    """
    Map an existing IP address to an interface ID
    args: netbox_obj, device_name, interface_name, ip4

    Where:
        netbox_obj - netbox object instance
        device_name - str() name of a device
        interface_name - str() name of an interface
        ip4 - str() ip address in A.B.C.D/E format
    """
    address = get_ip_address(netbox_obj, ip4)
    address.assigned_object_id = interface_id(netbox_obj, device_name, interface_name)
    address.assigned_object_type = "dcim.interface"
    address.save()
    func_name = getframeinfo(currentframe()).function
    print(
        f"{__name__}(v{OUR_VERSION}).{func_name}: device: {device_name}",
        f"interface {interface_name} ip_address {ip4}",
    )


def make_device_primary_ip(netbox_obj, device_name, ip4):
    """
    Make an ip address the primary address for a device by mapping
    the address ID to a device's primary_ip and primary_ip4.
    """
    device = get_device(netbox_obj, device_name)
    address_id = ip_address_id(netbox_obj, ip4)
    device.primary_ip = address_id
    device.primary_ip4 = address_id
    device.save()
    func_name = getframeinfo(currentframe()).function
    print(f"{__name__}(v{OUR_VERSION}).{func_name}: device: {device_name} ip4 {ip4}")


class Device:
    """
    create, update, and delete operations on netbox dcim.devices
    """

    def __init__(self, netbox_obj, info):
        self._netbox = netbox_obj
        self._info = info
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._args = {}

        self._mandatory_keys_create_or_update = set()
        self._mandatory_keys_create_or_update.add("device")
        self._mandatory_keys_create_or_update.add("role")
        self._mandatory_keys_create_or_update.add("type")

        self._mandatory_keys_delete = set()
        self._mandatory_keys_delete.add("device")
        self._fix_deprecations()

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _fix_deprecations(self):
        """
        We changed some key names for devices on 2022-09-29.
        If the caller presents the old key names, warn them and convert
        them to the new key names.
        TODO: remove this method on 2023-09-29
        """
        if "mgmt_interface" in self._info:
            self.log(
                "WARNING: 'devices: <device>: mgmt_interface' in your YAML file is deprecated",
                "Use 'devices: <device>: interface' instead.",
                "We will no longer accept the deprecated names after 2023-09-29",
            )
            self._info["interface"] = self._info["mgmt_interface"]
        if "name" in self._info:
            self.log(
                "WARNING: 'devices: <device>: name' in your YAML file is deprecated.",
                "Use 'devices: <device>: device' instead.",
                "We will no longer accept the deprecated names after 2023-09-29",
            )
            self._info["device"] = self._info["name"]

    def _validate_keys_delete(self):
        """
        ensure the caller has set all keys required by the delete method
        """
        for key in self._mandatory_keys_delete:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _validate_keys_create_or_update(self):
        """
        ensure the caller has set all keys required by the create and update methods
        """
        for key in self._mandatory_keys_create_or_update:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_cluster(self):
        """
        add device cluster, if any, to args
        """
        if self.cluster is None:
            return
        try:
            self._args["cluster"] = cluster_id(self._netbox, self.cluster)
        except Exception as _general_exception:
            self.log(
                f"exiting. unable to retrieve cluster_id from cluster {self.cluster}",
                f"Perhaps cluster {self.cluster} does not exist in Netbox?",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def _set_device_role(self):
        """
        add device role to args
        """
        self._args["device_role"] = role_id(self._netbox, self.device_role)

    def _set_device_type(self):
        """
        add device type to args
        """
        self._args["device_type"] = device_type_id(self._netbox, self.device_type)

    def _set_face(self):
        """
        add rack face, if any, to args
        """
        if self.face is not None:
            self._args["face"] = self.face

    def _set_location(self):
        """
        add location, if any, to args
        """
        if self.location is not None:
            self._args["location"] = location_id(self._netbox, self.location)

    def _set_name(self):
        """
        add device name to args
        """
        self._args["name"] = self._info["device"]

    def _set_position(self):
        """
        add rack position, if any, to args
        """
        if self.position is not None:
            self._args["position"] = self.position

    def _set_rack(self):
        """
        add rack, if any, to args
        """
        if self.rack is not None:
            self._args["rack"] = rack_id(self._netbox, self.rack)

    def _set_serial(self):
        """
        add the device's serial number, if any, to args
        """
        if self.serial is not None:
            self._args["serial"] = self.serial

    def _set_site(self):
        """
        add site to args
        """
        self._args["site"] = site_id(self._netbox, self.site)

    def _set_slug(self):
        """
        add slug to args
        """
        self._args["slug"] = create_slug(self._info["device"])

    def _set_tags(self):
        """
        add tags, if any, to args; converting them to netbox IDs
        """
        if self.tags is None:
            return
        self._args["tags"] = []
        for tag in self.tags:
            self._args["tags"].append(tag_id(self._netbox, tag))

    def _generate_args_create_or_update(self):
        """
        generate all supported arguments for create and update methods
        """
        self._set_cluster()
        self._set_device_role()
        self._set_device_type()
        self._set_name()
        self._set_site()
        self._set_slug()
        self._set_face()
        self._set_location()
        self._set_position()
        self._set_rack()
        self._set_serial()
        self._set_tags()

    def create(self):
        """
        create a device
        """
        self.log(f"{self.device}")
        try:
            self._netbox.dcim.devices.create(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to create device {self.device}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def update(self):
        """
        update a device
        """
        self.log(f"{self.device}")
        self._args["id"] = self.device_id
        try:
            self.device_object.update(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to update device {self.device}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def delete(self):
        """
        delete a device
        """
        self.log(f"{self.device}")
        self._validate_keys_delete()
        if self.device_object is None:
            self.log(f"Nothing to do, device {self.device} does not exist in netbox.")
            return
        try:
            self.device_object.delete()
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to delete device {self.device}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_keys_create_or_update()
        self._generate_args_create_or_update()
        if self.device_object is None:
            self.create()
        else:
            self.update()

    @property
    def cluster(self):
        """
        return the devices's cluster set by the caller.
        If the caller didn't set this, return None.
        """
        if "cluster" in self._info:
            return self._info["cluster"]
        return None

    @property
    def device_object(self):
        """
        return the netbox device object
        """
        return self._netbox.dcim.devices.get(name=self.device)

    @property
    def device_id(self):
        """
        return the netbox device ID
        """
        return self.device_object.id

    @property
    def device_role(self):
        """
        return the device's role set by the caller
        """
        return self._info["role"]

    @property
    def device_type(self):
        """
        return the device's type set by the caller
        """
        return self._info["type"]

    @property
    def face(self):
        """
        return the device's rack face set by the caller
        If the caller didn't set this, return None.
        """
        if "face" in self._info:
            return self._info["face"]
        return None

    @property
    def location(self):
        """
        return the device's location set by the caller
        If the caller didn't set this, return None.
        """
        if "location" in self._info:
            return self._info["location"]
        return None

    @property
    def name(self):
        """
        For backward-compatibility. Remove after 2023-09-29
        """
        return self._info["device"]

    @property
    def device(self):
        """
        return the device's name set by the caller
        """
        return self._info["device"]

    @property
    def position(self):
        """
        return the device's rack position set by the caller
        If the caller didn't set this, return None.
        """
        if "position" in self._info:
            return self._info["position"]
        return None

    @property
    def rack(self):
        """
        return the device's rack set by the caller
        If the caller didn't set this, return None.
        """
        if "rack" in self._info:
            return self._info["rack"]
        return None

    @property
    def serial(self):
        """
        return the device's serial number set by the caller
        If the caller didn't set this, return None.
        """
        if "serial" in self._info:
            return self._info["serial"]
        return None

    @property
    def site(self):
        """
        Mandatory. return the device's site set by the caller
        """
        return self._info["site"]

    @property
    def slug(self):
        """
        return the slug (url friendly name) of the device set by the caller.
        If the caller didn't set this, we set it in self._set_slug()
        """
        if "slug" in self._info:
            return self._info["slug"]
        return None

    @property
    def tags(self):
        """
        return the list of tag names set by the caller.
        If the caller didn't set this, return None.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
