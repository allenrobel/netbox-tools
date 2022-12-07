"""
Name: device_type.py
Description: Create, update, delete netbox device types
"""
from inspect import stack
import sys
from netbox_tools.common import manufacturer_id
from netbox_tools.common import create_slug
from netbox_tools.common import tag_id

OUR_VERSION = 106


class DeviceType:
    """
    Create, update, delete netbox device types

    from netbox_tools.common import netbox
    netbox_instance = netbox()
    d = DeviceType(netbox_instance, info_dict)
    d.create_or_update()
    d.delete()

    Where info_dict contains the following structure

    device_types:
    CISCO-UNKNOWN:
        model: CISCO-UNKNOWN
        manufacturer: cisco
    CISCO-2600:
        model: CISCO-2600
        manufacturer: cisco
        u_height: 1
    """

    def __init__(self, netbox_obj, info):
        self._netbox_obj = netbox_obj
        self._info = info
        self._classname = __class__.__name__
        self.lib_version = OUR_VERSION
        self._args = {}

        self._mandatory_create_update_keys = set()
        self._mandatory_create_update_keys.add("manufacturer")
        self._mandatory_create_update_keys.add("model")

        self._mandatory_delete_keys = set()
        self._mandatory_delete_keys.add("model")

        self._optional_keys = set()  # this is FYI only and is not used
        self._optional_keys.add("comments")
        self._optional_keys.add("slug")
        self._optional_keys.add("tags")

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _validate_delete_keys(self):
        for key in self._mandatory_delete_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _validate_create_update_keys(self):
        for key in self._mandatory_create_update_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_comments(self):
        """
        add comments to args, if present
        """
        if self.comments is not None:
            self._args["comments"] = self.comments

    def _set_manufacturer(self):
        """
        add manufacturer to args
        """
        self._args["manufacturer"] = manufacturer_id(self._netbox_obj, self.manufacturer)

    def _set_model(self):
        """
        add model to args
        """
        self._args["model"] = self.model

    def _set_slug(self):
        """
        populate args with a url-friendly name for the device_type
        If the caller has not set the slug, we do it here
        """
        if self.slug is None:
            self._args["slug"] = create_slug(self.model)
        else:
            self._args["slug"] = self.slug

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
        self._set_comments()
        self._set_manufacturer()
        self._set_model()
        self._set_slug()
        self._set_tags()

    def delete(self):
        """
        delete a device_type
        """
        self._validate_delete_keys()
        if self.device_type_obj is None:
            self.log(
                f"Nothing to do. device_type {self.model} does not exist in netbox."
            )
            return
        self.log(f"{self.model}")
        try:
            self.device_type_obj.delete()
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to delete device_type {self.model}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def create(self):
        """
        create a device_type
        """
        self.log(f"{self.model}")
        try:
            self._netbox_obj.dcim.device_types.create(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to create device_type {self.model}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def update(self):
        """
        update a device_type
        """
        self.log(f"{self.model}")
        if self.device_type_id is None:
            self.log(f"{self.model} does not exist in netbox. Skipping.")
            return
        self._args["id"] = self.device_type_id
        try:
            self.device_type_obj.update(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to update device_type {self.model}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_create_update_keys()
        self._generate_create_update_args()
        if self.device_type_obj is None:
            self.create()
        else:
            self.update()

    @property
    def comments(self):
        """
        free-form comments associated with device_type.
        If the caller set comments, return it.  Else return None.
        """
        if "comments" in self._info:
            return self._info["comments"]
        return None

    @property
    def manufacturer(self):
        """
        Mandatory. Return the manufacturer set by the caller.
        """
        return self._info["manufacturer"]

    @property
    def model(self):
        """
        Mandatory. Return the model (device_type) set by the caller.
        """
        return self._info["model"]

    @property
    def slug(self):
        """
        set the slug (url friendly name) of the device_type.  If this
        is not set by the caller, we set it in self._set_slug()
        """
        if "slug" in self._info:
            return self._info["slug"]
        return None

    @property
    def device_type_obj(self):
        """
        return an instance of the netbox device_type
        If the device_type does not exist, None will be returned
        """
        return self._netbox_obj.dcim.device_types.get(model=self.model)

    @property
    def device_type_id(self):
        """
        return the netbox ID of the device_type
        If the device_type does not exist, None will be returned
        """
        if self.device_type_obj is None:
            return None
        return self.device_type_obj.id

    @property
    def tags(self):
        """
        A list of tag names to associate with the console_server_port.
        If tags is set, return it.  Else return None.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
