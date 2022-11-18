"""
Name: console_server_port.py
Description: Create, update, delete operations on netbox /dcim/console-server-ports/ endpoint
"""
from inspect import stack
import sys
from netbox_tools.common import device_id, tag_id

OUR_VERSION = 102


class ConsoleServerPort:
    """
    create, update, delete Netbox console server ports

    from netbox_tools.common import netbox
    netbox_instance = netbox()
    c = ConsoleServerPort(netbox_instance, info_dict)
    c.create_or_update()
    c.delete()

    Where info_dict contains the following structure

    console_server_ports:
    ts_1_2003:
        device: ts_1
        label: dc-115
        mark_connected: False
        port: 2003
        port_speed: 9600
        port_type: rj-45
        description: bgw_3
        tags:
        - admin

    TODO: 2022-11-18: add support for module
    """

    def __init__(self, netbox_obj, info):
        self._netbox = netbox_obj
        self._info = info
        self._classname = __class__.__name__
        self.lib_version = OUR_VERSION
        self._args = {}

        self._mandatory_create_update_keys = set()
        self._mandatory_create_update_keys.add("device")
        self._mandatory_create_update_keys.add("port")

        self._mandatory_delete_keys = set()
        self._mandatory_delete_keys.add("device")
        self._mandatory_delete_keys.add("port")

        self._optional_keys = set()
        self._optional_keys.add("description")
        self._optional_keys.add("mark_connected")
        self._optional_keys.add("port_speed")
        self._optional_keys.add("port_type")

        self.port_speed_to_label = {}
        self.port_speed_to_label[1200] = "1200 bps"
        self.port_speed_to_label[2400] = "2400 bps"
        self.port_speed_to_label[4800] = "4800 bps"
        self.port_speed_to_label[9600] = "9600 bps"
        self.port_speed_to_label[19200] = "19.2 kbps"
        self.port_speed_to_label[38400] = "38.4 kbps"
        self.port_speed_to_label[57600] = "57.6 kbps"
        self.port_speed_to_label[115200] = "115.2 kbps"

        self.port_type_to_label = {}
        self.port_type_to_label["de-9"] = "DE-9"
        self.port_type_to_label["db-25"] = "DB-25"
        self.port_type_to_label["rj-11"] = "RJ-11"
        self.port_type_to_label["rj-12"] = "RJ-12"
        self.port_type_to_label["rj-45"] = "RJ-45"
        self.port_type_to_label["mini-din-8"] = "Mini-DIN 8"
        self.port_type_to_label["usb-a"] = "USB Type A"
        self.port_type_to_label["usb-b"] = "USB Type B"
        self.port_type_to_label["usb-c"] = "USB Type C"
        self.port_type_to_label["usb-mini-a"] = "USB Mini A"
        self.port_type_to_label["usb-mini-b"] = "USB Mini B"
        self.port_type_to_label["usb-micro-a"] = "USB Micro A"
        self.port_type_to_label["usb-micro-b"] = "USB Micro B"
        self.port_type_to_label["usb-micro-ab"] = "USB Micro AB"
        self.port_type_to_label["other"] = "Other"

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _validate_delete_keys(self):
        """
        verify that all mandatory keys for delete() are present
        """
        for key in self._mandatory_delete_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _validate_create_update_keys(self):
        """
        verify that all mandatory keys for create() and update() are present
        """
        for key in self._mandatory_create_update_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_description(self):
        """
        add description to args, if present
        """
        if self.description is not None:
            self._args["description"] = self.description

    def _set_device(self):
        """
        add device to args
        """
        self._args["device"] = device_id(self._netbox, self.device)

    def _set_mark_connected(self):
        """
        add mark_connected to args, if present
        """
        if self.mark_connected is None:
            return
        if isinstance(self.mark_connected, bool):
            self._args["mark_connected"] = self.mark_connected
        self.log(
            f"exiting. Expected boolean for mark_connected. Got {self.mark_connected}"
        )
        sys.exit(1)

    def _set_port_name(self):
        """
        add name to args
        """
        self._args["name"] = self.port

    def _set_port_speed(self):
        """
        validate speed and add to args, if present
        """
        if self.port_speed is None:
            return
        if self.port_speed not in self.port_speed_to_label:
            valid_values = ",".join(self.port_speed_to_label.keys())
            self.log(
                f"exiting. Unknown port_speed {self.port_speed}.",
                f"Valid values are: {valid_values}",
            )
            sys.exit(1)
        self._args["speed"] = self.port_speed

    def _set_port_type(self):
        """
        validate port type and add to args, if present
        """
        if self.port_type is None:
            return
        if self.port_type not in self.port_type_to_label:
            valid_values = ",".join(self.port_type_to_label.keys())
            self.log(
                f"exiting. Unknown port_type {self.port_type}",
                f"Valid values are: {valid_values}",
            )
            sys.exit(1)
        self._args["type"] = self.port_type

    def _set_tags(self):
        """
        set the console_port's tags, if any; converting them to netbox ids
        """
        if self.tags is None:
            return
        self._args["tags"] = []
        for tag in self.tags:
            self._args["tags"].append(tag_id(self._netbox, tag))

    def generate_create_update_args(self):
        """
        generate all supported arguments for create() and update() methods
        """
        self._set_description()
        self._set_device()
        self._set_mark_connected()
        self._set_port_name()
        self._set_port_speed()
        self._set_port_type()
        self._set_tags()

    def delete(self):
        """
        delete a console_server_port
        """
        self._validate_delete_keys()
        if self.console_server_port_object is None:
            self.log(
                f"Nothing to do. Device {self.device} port {self.port} does not exist in netbox."
            )
            return
        self.log(f"device {self.device} port {self.port}")
        try:
            self.console_server_port_object.delete()
        except Exception as _general_error:
            self.log(
                f"Error. Unable to delete device {self.device} port {self.port}.",
                f"Exception detail: {_general_error}",
            )
            return

    def create(self):
        """
        create a console_server_port
        """
        self.log(f"device {self.device} port {self.port}")
        try:
            self._netbox.dcim.console_server_ports.create(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to create device {self.device} port {self.port}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def update(self):
        """
        update a console_server_port
        """
        self.log(f"device {self.device} port {self.port}")
        try:
            self.console_server_port_object.update(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to update device {self.device} port {self.port}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_create_update_keys()
        self.generate_create_update_args()
        if self.console_server_port_object is None:
            self.create()
        else:
            self.update()

    @property
    def console_server_port_object(self):
        """
        return a console_server_port object by searching for
        the console_server_port's device and name
        """
        try:
            return self._netbox.dcim.console_server_ports.get(
                device=self.device, name=self.port
            )
        except Exception as _general_error:
            self.log(
                "exiting. dcim.console_server_ports.get() failed for device",
                f"{self.device} port {self.port}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    @property
    def description(self):
        """
        A free-form description of the console_server_port.
        If the caller set description, return it.  Else return None.
        """
        if "description" in self._info:
            return self._info["description"]
        return None

    @property
    def device(self):
        """
        Mandatory. Return the device name set by the caller.
        """
        return self._info["device"]

    @property
    def label(self):
        """
        A physical label attached to the console port.
        If label is set, return it.  Else return None.
        """
        if "label" in self._info:
            return self._info["label"]
        return None

    @property
    def mark_connected(self):
        """
        Treat as if a cable is connected.
        If mark_connected is set, return it.  Else return None.
        """
        if "mark_connected" in self._info:
            return self._info["mark_connected"]
        return None

    @property
    def port(self):
        """
        Mandatory. The console server port name. This is used to populate the "name" argument.
        """
        return self._info["port"]

    @property
    def port_speed(self):
        """
        The speed of the console port in bits per second.
        If the caller set port_speed, return it.  Else return None.
        """
        if "port_speed" in self._info:
            return self._info["port_speed"]
        return None

    @property
    def port_type(self):
        """
        If the caller set port_type, return it.  Else return None.
        """
        if "port_type" in self._info:
            return self._info["port_type"]
        return None

    @property
    def tags(self):
        """
        A list of tag names to associate with the console_server_port.
        If tags is set, return it.  Else return None.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
