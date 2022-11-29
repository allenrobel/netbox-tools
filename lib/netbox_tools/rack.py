"""
Name: rack.py
Description: create, update, and delete operations on netbox rack
"""
from inspect import stack
import sys
from netbox_tools.common import location_id, site_id, tag_id

OUR_VERSION = 101

class Rack:
    """
    create, update, and delete operations on netbox rack
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_delete_keys = set()
        self._mandatory_delete_keys.add("name")
        self._mandatory_create_update_keys = set()
        self._mandatory_create_update_keys.add("location")
        self._mandatory_create_update_keys.add("name")
        self._mandatory_create_update_keys.add("site")
        self._optional_keys = set()  # these are FYI only i.e. not used in this class
        self._optional_keys.add("comments")
        self._optional_keys.add("tags")
        self._optional_keys.add("u_height")

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _validate_delete_keys(self):
        """
        Verify that all mandatory delete operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_delete_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _validate_keys_create_update(self):
        """
        Verify that all mandatory create/update operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_create_update_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_comments(self):
        """
        Add comments, if any, to args
        """
        if self.comments is None:
            return
        self._args["comments"] = self.comments

    def _set_location(self):
        """
        Convert location to netbox location ID, and add to args
        """
        self._args["location"] = location_id(self._netbox_obj, self.location)

    def _set_name(self):
        """
        Add name to args
        """
        self._args["name"] = self.name

    def _set_site(self):
        """
        Convert site to netbox site ID, and add to args
        """
        self._args["site"] = site_id(self._netbox_obj, self.site)

    def _set_tags(self):
        """
        Add tags, if any, to args; converting them to netbox IDs
        """
        if self.tags is None:
            return
        self._args["tags"] = []
        for tag in self.tags:
            self._args["tags"].append(tag_id(self._netbox_obj, tag))

    def _set_u_height(self):
        """
        Add u_height, if any, to args
        """
        if self.u_height is None:
            return
        self._args["u_height"] = self.u_height

    def _generate_args_create_update(self):
        """
        Generate all supported arguments for create and update methods
        """
        self._set_comments()
        self._set_location()
        self._set_name()
        self._set_tags()
        self._set_u_height()

    def delete(self):
        """
        delete a rack
        """
        self._validate_delete_keys()
        if self.rack_obj is None:
            self.log(f"Nothing to do. Rack {self.name} does not exist in netbox.")
            return
        self.log(f"{self.name}")
        try:
            self.rack_obj.delete()
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to delete rack {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create(self):
        """
        create a rack
        """
        self.log(f"{self.name}")
        try:
            self._netbox_obj.dcim.racks.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to create rack {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update a rack
        """
        if self.rack_id is None:
            self.log(f"Skipping. rack {self.name} does not exist in Netbox")
            return
        self.log(f"{self.name}")
        self._args["id"] = self.rack_id
        try:
            self.rack_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to update rack {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_keys_create_update()
        self._generate_args_create_update()
        if self.rack_obj is None:
            self.create()
        else:
            self.update()

    @property
    def comments(self):
        """
        Return comments set by the caller.
        Return None if the caller didn't set this.
        """
        if "comments" in self._info:
            return self._info["comments"]
        return None

    @property
    def name(self):
        """
        Return the rack name set by the caller.
        """
        return self._info["name"]

    @property
    def location(self):
        """
        Return the rack location set by the caller.
        """
        return self._info["location"]

    @property
    def rack_obj(self):
        """
        Return the rack object assocated with rack name.
        Netbox will return None if the rack name does not exist.
        """
        return self._netbox_obj.dcim.racks.get(name=self.name)

    @property
    def rack_id(self):
        """
        Return the Netbox ID of the rack associated with
        rack name set by the caller.
        Return None if the rack does not exist
        """
        if self.rack_obj is not None:
            return self.rack_obj.id
        return None

    @property
    def site(self):
        """
        Return the site set by the caller.
        """
        return self._info["site"]

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
    def u_height(self):
        """
        Return the rack u_height set by the caller.
        If the caller didn't set this, return None.
        """
        if "u_height" in self._info:
            return self._info["u_height"]
        return None
