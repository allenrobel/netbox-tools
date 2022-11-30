"""
Name: location.py
Description: create and update operations on netbox location
"""
from inspect import stack
import sys
from netbox_tools.common import create_slug
from netbox_tools.common import tag_id
from netbox_tools.common import site_id

OUR_VERSION = 102


class Location:
    """
    create and update operations on netbox location
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self.mandatory_keys_create_update = set()
        self.mandatory_keys_create_update.add("name")
        self.mandatory_keys_create_update.add("site")

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _validate_keys_create_update(self):
        """
        Verify that all mandatory create/update operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self.mandatory_keys_create_update:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_name(self):
        """
        Add name to args
        """
        self._args["name"] = self.name

    def _set_site(self):
        """
        Add site to args
        """
        self._args["site"] = site_id(self._netbox_obj, self.site)

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
            tid = tag_id(self._netbox_obj, tag)
            if tid is None:
                self.log(f"tag {tag} not found in Netbox.  Skipping.")
                continue
            self._args["tags"].append(tid)

    def _generate_args_create_update(self):
        """
        Generate all supported arguments for create and update methods
        """
        self._set_name()
        self._set_site()
        self._set_slug()
        self._set_tags()

    def delete(self):
        """
        delete a location
        """
        self.log(f"location {self.name}")
        try:
            self.location_obj.delete()
        except Exception as _general_exception:
            self.log(
                f"WARNING. Unable to delete location {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            return

    def create(self):
        """
        create a location
        """
        self.log(f"location {self.name}")
        try:
            self._netbox_obj.dcim.locations.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"WARNING. Unable to create location {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update a location
        """
        self.log(f"location {self.name}")
        self._args["id"] = self.location_id
        try:
            self.location_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"WARNING. Unable to update location {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_keys_create_update()
        self._generate_args_create_update()
        if self.location_obj is None:
            self.create()
        else:
            self.update()

    @property
    def location_obj(self):
        """
        Return the location object assocated with the location
        name set by the caller.
        Netbox will return None if the location is not found.
        """
        return self._netbox_obj.dcim.locations.get(name=self.name)

    @property
    def location_id(self):
        """
        Return the Netbox ID of the location object assocated with the location
        name set by the caller.
        Return None, if the location is not found in Netbox.
        """
        if self.location_obj is not None:
            return self.location_obj.id
        return None

    @property
    def name(self):
        """
        Return name set by the caller.
        """
        return self._info["name"]

    @property
    def site(self):
        """
        Return the site set by the caller.
        If the caller didn't set this, return None.
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
