"""
Name: vlan_group.py
Description: create, update, and delete operations on netbox vlan_group
"""
from inspect import stack
import sys
from netbox_tools.common import tag_id
from netbox_tools.common import create_slug

OUR_VERSION = 102


class VlanGroup:
    """
    create, update, and delete operations on netbox vlan_group
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_keys = set()
        self._mandatory_keys.add("vlan_group")
        self._optional_keys = set()  # FYI only.  Not used in this class.
        self._optional_keys.add("description")
        self._optional_keys.add("max_vid")
        self._optional_keys.add("min_vid")
        self._optional_keys.add("tags")

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _validate_keys(self):
        """
        Verify that all mandatory create/update operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_description(self):
        """
        Add description to args, if it is set.
        """
        if self.description is not None:
            self._args["description"] = self.description

    def _set_max_vid(self):
        """
        Add max_vid to args, if it is set.
        """
        if self.max_vid is not None:
            self._args["max_vid"] = self.max_vid

    def _set_min_vid(self):
        """
        Add min_vid to args, if it is set.
        """
        if self.min_vid is not None:
            self._args["min_vid"] = self.min_vid

    def _set_name(self):
        """
        Add vlan_group name to args.
        """
        self._args["name"] = self.vlan_group_name

    def _set_slug(self):
        """
        Add slug to args
        """
        self._args["slug"] = create_slug(self.vlan_group_name)

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
        self._set_description()
        self._set_name()
        self._set_max_vid()
        self._set_min_vid()
        self._set_slug()
        self._set_tags()

    def delete(self):
        """
        delete vlan_group
        """
        self.log(f"{self.vlan_group_name}")
        if self.vlan_group_obj is None:
            self.log(
                f"Nothing to do. VlanGroup {self.vlan_group_name} does not exist in netbox."
            )
            return
        try:
            self.vlan_group_obj.delete()
        except Exception as _general_exception:
            self.log(
                f"WARNING. Unable to delete VlanGroup {self.vlan_group_name}.",
                f"Exception detail: {_general_exception}",
            )
            return

    def create(self):
        """
        create vlan_group
        """
        self.log(f"{self.vlan_group_name}")
        try:
            self._netbox_obj.ipam.vlan_groups.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to create VlanGroup {self.vlan_group_name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update vlan_group
        """
        self.log(f"{self.vlan_group_name}")
        self._args["id"] = self.vlan_group_id
        try:
            self.vlan_group_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to update VlanGroup {self.vlan_group_name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_keys()
        self._generate_args()
        if self.vlan_group_obj is None:
            self.create()
        else:
            self.update()

    @property
    def max_vid(self):
        """
        Return max_vid (vlan id) set by the caller.
        Return None if the caller did not set this.
        """
        if "max_vid" in self._info:
            return self._info["max_vid"]
        return None

    @property
    def min_vid(self):
        """
        Return min_vid (vlan id) set by the caller.
        Return None if the caller did not set this.
        """
        if "min_vid" in self._info:
            return self._info["min_vid"]
        return None

    @property
    def vlan_group_name(self):
        """
        Return vlan_group name set by the caller.
        """
        return self._info["vlan_group"]

    @property
    def description(self):
        """
        Return the description set by the caller.
        Return None if the caller did not set this.
        """
        if "description" in self._info:
            return self._info["description"]
        return None

    @property
    def vlan_group_obj(self):
        """
        Return the Netbox object associated with the vlan_group set by the caller.
        Exit with error if this object cannot be retrieved from Netbox.
        """
        try:
            return self._netbox_obj.ipam.vlan_groups.get(name=self.vlan_group_name)
        except Exception as _general_exception:
            self.log(
                "exiting. Unable to retrieve vlan_group object from Netbox",
                f"for vlan_group name {self.vlan_group_name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    @property
    def vlan_group_id(self):
        """
        Return the Netbox ID of the vlan_group object associated with the
        vlan group set by the caller.
        If the vlan_group_obj cannot be retrieved from Netbox, the vlan_group_obj property
        will exit with error.
        """
        return self.vlan_group_obj.id

    @property
    def tags(self):
        """
        Return the list of tag names set by the caller.
        Return None if the caller didn't set this.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
