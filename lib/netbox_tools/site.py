"""
Name: site.py
Description: create, update, and delete operations on netbox site
"""

from inspect import stack
import sys
from netbox_tools.common import tag_id
from netbox_tools.common import create_slug

OUR_VERSION = 101


class Site:
    """
    create, update, and delete operations on netbox site
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_keys_create_update = set()
        self._mandatory_keys_create_update.add("name")
        self._mandatory_keys_delete = set()
        self._mandatory_keys_delete.add("name")
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
        """
        Generate all supported arguments for create and update methods
        """
        self._set_description()
        self._set_name()
        self._set_slug()
        self._set_tags()

    def delete(self):
        """
        delete a site
        """
        self._validate_keys_delete()
        if self.site_obj is None:
            self.log(f"Nothing to do. Role {self.name} does not exist in netbox.")
            return
        self.log(f"{self.name}")
        try:
            self.site_obj.delete()
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to delete site {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create(self):
        """
        create a site
        """
        self.log(f"{self.name}")
        try:
            self._netbox_obj.dcim.sites.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to create site {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update a site
        """
        if self.site_id is None:
            self.log(f"Skipping. site {self.name} does not exist in Netbox")
            return
        self.log(f"{self.name}")
        self._args["id"] = self.site_id
        try:
            self.site_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to update site {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_keys_create_update()
        self._generate_args()
        if self.site_obj is None:
            self.create()
        else:
            self.update()

    @property
    def name(self):
        """
        Return name set by the caller.
        """
        return self._info["name"]

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
    def site_obj(self):
        """
        Return site object associated with name set by the caller.
        Netbox will return None if the site does not exist.
        """
        return self._netbox_obj.dcim.sites.get(name=self.name)

    @property
    def site_id(self):
        """
        Return Netbox ID for the site object associated with site name set by the caller.
        Return None if the site doesn't exist in Netbox.
        """
        if self.site_obj is not None:
            return self.site_obj.id
        return None

    @property
    def tags(self):
        """
        Return the list of tag names set by the caller.
        Return none if the caller didn't set this.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
