"""
Name: vlan.py
Description: create, update, and delete operations on netbox vlan
"""
from inspect import stack
import sys
from netbox_tools.common import create_slug, role_id, site_id, tag_id, vlan_group_id

OUR_VERSION = 102


class Vlan:
    """
    create, update, and delete operations on netbox vlan
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self.mandatory_keys = set()
        self.mandatory_keys.add("vid")
        self.mandatory_keys.add("vlan_name")
        self.optional_keys = set()  # FYI only.  Not used in this class.
        self.optional_keys.add("description")
        self.optional_keys.add("group")
        self.optional_keys.add("role")
        self.optional_keys.add("site")
        self.optional_keys.add("status")
        self.optional_keys.add("tags")
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
        retrieve valid vlan choices from the users netbox instance
        """
        self._valid_choices = {}
        choices_dict = self._netbox_obj.ipam.vlans.choices()
        for item in choices_dict:
            valid_values = choices_dict[item]
            self._valid_choices[item] = [item["value"] for item in valid_values]

    def validate_keys(self):
        """
        Verify that all mandatory create/update operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self.mandatory_keys:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _set_description(self):
        """
        Add description to args, if it is set.
        """
        if self.description is not None:
            self._args["description"] = self.description

    def _set_group(self):
        """
        Add vlan group to args, converting it to its associated netbox id, if it is set.
        """
        if self.group is not None:
            self._args["group"] = vlan_group_id(self._netbox_obj, self.group)

    def _set_name(self):
        """
        Add vlan name to args.
        """
        self._args["name"] = self.vlan_name

    def _set_role(self):
        """
        Add vlan role to args, converting to netbox ID, if it is set.
        """
        if self.role is None:
            return
        try:
            self._args["role"] = role_id(self._netbox_obj, self.role)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to set role ID for role {self.role}"
                "Does this role exist in Netbox?"
            )
            sys.exit(1)

    def _set_site(self):
        """
        Add site to args, converting to site ID, if it is set.
        """
        if self.site is not None:
            self._args["site"] = site_id(self._netbox_obj, self.site)

    def _set_slug(self):
        """
        Add slug to args
        """
        self._args["slug"] = create_slug(self.vlan_name)

    def _set_status(self):
        """
        Add status to args, if it is set.
        """
        if self.status is not None:
            self._args["status"] = self.status

    def _set_tags(self):
        """
        Add tags, if any, to args; converting them to netbox IDs.
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

    def _set_vid(self):
        """
        Add vlan ID to args.
        """
        self._args["vid"] = self.vid

    def _verify_mutex_args(self):
        """
        Verify that only one mutually-exclusive argument is set.
        Exit if this is not the case.
        """
        if self.site is not None and self.group is not None:
            self.log(
                f"exiting {self.vlan_name}. site and group are mutually-exclusive.",
                f"Got group {self.group}, site {self.site}",
            )
            sys.exit(1)

    def generate_args(self):
        """
        Generate all supported arguments for create and update methods
        """
        self._verify_mutex_args()
        self._set_description()
        self._set_group()
        self._set_name()
        self._set_role()
        self._set_site()
        self._set_slug()
        self._set_status()
        self._set_tags()
        self._set_vid()

    def delete(self):
        """
        delete vlan
        """
        self.log(f"{self.vlan_name}")
        if self.vlan_obj is None:
            self.log(f"Nothing to do. Vlan {self.vlan_name} does not exist in netbox.")
            return
        try:
            self.vlan_obj.delete()
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to delete Vlan {self.vlan_name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create(self):
        """
        create vlan
        """
        self.log(f"{self.vlan_name}")
        try:
            self._netbox_obj.ipam.vlans.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to create Vlan {self.vlan_name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update vlan
        """
        self.log(f"{self.vlan_name}")
        self._args["id"] = self.vlan_id
        try:
            self.vlan_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"exiting. Unable to update Vlan {self.vlan_name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self.validate_keys()
        self.generate_args()
        if self.vlan_obj is None:
            self.create()
        else:
            self.update()

    @property
    def description(self):
        """
        Return the vlan description set by the caller.
        Return None if the caller did not set this.
        """
        if "description" in self._info:
            return self._info["description"]
        return None

    @property
    def group(self):
        """
        Return the vlan group set by the caller.
        Return None if the caller did not set this.
        """
        if "group" in self._info:
            return self._info["group"]
        return None

    @property
    def role(self):
        """
        Return the vlan role set by the caller.
        Return None if the caller did not set this.
        """
        if "role" in self._info:
            return self._info["role"]
        return None

    @property
    def site(self):
        """
        Return the vlan site set by the caller.
        Return None if the caller did not set this.
        """
        if "site" in self._info:
            return self._info["site"]
        return None

    @property
    def status(self):
        """
        Return the vlan status set by the caller.
        Return None if the caller did not set this.
        """
        if "status" in self._info:
            return self._info["status"]
        return None

    @property
    def vid(self):
        """
        Return the vlan ID set by the caller.
        Return None if the caller did not set this.
        """
        if "vid" in self._info:
            return self._info["vid"]
        return None

    @property
    def vlan_name(self):
        """
        Return the vlan name set by the caller.
        Return None if the caller did not set this.
        """
        if "vlan_name" in self._info:
            return self._info["vlan_name"]
        return None

    @property
    def vlan_obj(self):
        """
        Return the Netbox object associated with the vlan set by the caller.
        Exit with error if this object cannot be retrieved from Netbox.
        """
        try:
            return self._netbox_obj.ipam.vlans.get(name=self.vlan_name)
        except Exception as _general_exception:
            self.log(
                "exiting. Unable to retrieve vlan object from Netbox",
                f"for vlan name {self.vlan_name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    @property
    def vlan_id(self):
        """
        Return the Netbox ID of the vlan object associated with the vlan set by the caller.
        If the vlan_obj cannot be retrieved from Netbox, the vlan_obj property
        will exit with error.
        """
        return self.vlan_obj.id

    @property
    def tags(self):
        """
        Return the list of tag names set by the caller.
        If the caller didn't set this, return None.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
