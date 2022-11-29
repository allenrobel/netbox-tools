"""
Name: role.py
Description: create, update, and delete operations on netbox device roles
"""
from inspect import stack
import sys
from netbox_tools.common import create_slug, tag_id
from netbox_tools.colors import color_to_rgb

OUR_VERSION = 101


class Role:
    """
    create, update, and delete operations on netbox device roles
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_keys = set()
        self._mandatory_keys.add("color")
        self._mandatory_keys.add("name")
        self._optional_keys = set()  # FYI only.  Not used in this class.
        self._optional_keys.add("description")
        self._optional_keys.add("tags")

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _validate_keys(self):
        for key in self._mandatory_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_color(self):
        """
        Add color to args
        """
        self._args["color"] = self.rgb

    def _set_description(self):
        """
        Add description, if any, to args
        """
        if self.description is None:
            return
        self._args["description"] = self.description

    def _set_name(self):
        """
        Add name to args
        """
        self._args["name"] = self.name

    def _set_slug(self):
        """
        Add slug to args
        """
        self._args["slug"] = create_slug(self.name)

    def _set_tags(self):
        """
        Add tags, if any, to args; converting them to netbox IDs
        """
        if self.tags is None:
            return
        self._args["tags"] = []
        for tag in self.tags:
            self._args["tags"].append(tag_id(self._netbox_obj, tag))

    def _generate_args(self):
        self._set_color()
        self._set_description()
        self._set_name()
        self._set_slug()
        self._set_tags()

    def delete(self):
        """
        delete a role
        """
        if self.role_obj is None:
            self.log(f"Nothing to do. Role {self.name} does not exist in netbox.")
            return
        self.log(f"{self.name}")
        try:
            self.role_obj.delete()
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to delete role {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create(self):
        """
        create a role
        """
        self.log(f"{self.name}")
        try:
            self._netbox_obj.dcim.device_roles.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to create role {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update a role
        """
        if self.role_id is None:
            self.log(f"Skipping. role {self.name} does not exist in Netbox")
            return
        self.log(f"{self.name}")
        self._args["id"] = self.role_id
        try:
            self.role_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to update role {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_keys()
        self._generate_args()
        if self.role_obj is None:
            self.create()
        else:
            self.update()

    @property
    def color(self):
        """
        Return color set by the caller.
        """
        return self._info["color"]

    @property
    def description(self):
        """
        Return description set by the caller.
        Return None if the caller didn't set this.
        """
        if "description" in self._info:
            return self._info["description"]
        return None

    @property
    def name(self):
        """
        Return name set by the caller.
        """
        return self._info["name"]

    @property
    def rgb(self):
        """
        Return rgb assocated with color set by the caller.
        """
        return color_to_rgb(self._info["color"])

    @property
    def role_obj(self):
        """
        Return role object associated with name set by the caller.
        """
        return self._netbox_obj.dcim.device_roles.get(name=self.name)

    @property
    def role_id(self):
        """
        Return Netbox ID for the role object associated with role name
        set by the caller.
        """
        if self.role_obj is not None:
            return self.role_obj.id
        return None

    @property
    def slug(self):
        """
        Return slug (url friendly name) for the role name
        set by the caller.
        """
        return create_slug(self.name)

    @property
    def tags(self):
        """
        Return the list of tag names set by the caller.
        If the caller didn't set this, return None.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
