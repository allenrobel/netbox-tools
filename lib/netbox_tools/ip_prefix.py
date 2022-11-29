"""
Name: ip_prefix.py
Description: Create, update, delete operations on netbox ip_prefix
"""
from inspect import stack
import sys
from netbox_tools.common import site_id, vlan_vid_to_id

OUR_VERSION = 102


class IpPrefix:
    """
    Create, update, delete operations on netbox ip_prefix
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_keys = set()
        self._mandatory_keys.add("prefix")
        self._optional_keys = set()
        self._optional_keys.add("description")
        self._optional_keys.add("site")
        self._optional_keys.add("status")
        self._optional_keys.add("vlan")
        self._optional_keys.add("tags")
        self.default_status = "active"
        self._validate_keys()
        self._generate_args()

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

    def _generate_args(self):
        """
        Generate all supported arguments for create and update methods
        """
        self._args["prefix"] = self.prefix
        if self.description is not None:
            self._args["description"] = self.description
        if self.site is not None:
            if self._site_id is None:
                self.log(
                    f"exiting. prefix {self.prefix} site {self.site} does not exist in netbox.",
                    "Either create the site first, or do not specify a site for this prefix.",
                )
                sys.exit(1)
            self._args["site"] = self._site_id
        if self.status is not None:
            self._args["status"] = self.status
        else:
            self._args["status"] = self.default_status
        if self.vlan is not None:
            self._args["vlan"] = self.vlan_id

    def delete(self):
        """
        delete a prefix
        """
        self.log(f"prefix {self.prefix}")
        if self.prefix_object is None:
            self.log(f"Nothing to do. Prefix {self.prefix} does not exist in netbox")
            return
        try:
            self.prefix_object.delete()
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to delete prefix {self.prefix}",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create(self):
        """
        create a prefix
        """
        self.log(f"prefix {self.prefix}")
        try:
            self._netbox_obj.ipam.prefixes.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to create prefix {self.prefix}",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update a prefix
        """
        self.log(f"prefix {self.prefix}")
        self._args["id"] = self.prefix_id
        try:
            self.prefix_object.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to update prefix {self.prefix}",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        if self.prefix_object is None:
            self.create()
        else:
            self.update()

    @property
    def description(self):
        """
        Return the prefix description set by the caller.
        If the caller didn't set this, return None.
        """
        if "description" in self._info:
            return self._info["description"]
        return None

    @property
    def prefix_object(self):
        """
        Return the netbox prefix object associated with the
        prefix set by the caller. If the caller didn't set prefix,
        this is caught in _validate_keys, so no need here for error handling.
        """
        return self._netbox_obj.ipam.prefixes.get(prefix=self.prefix)

    @property
    def prefix(self):
        """
        Return the prefix set by the caller. If the caller didn't set prefix,
        this is caught in _validate_keys, so no need here for error handling.
        """
        return self._info["prefix"]

    @property
    def prefix_id(self):
        """
        Return the netbox prefix ID associated with the
        prefix set by the caller. If the caller didn't set prefix,
        this is caught in _validate_keys, so no need here for error handling.
        """
        if self.prefix_object is None:
            self.log(
                f"exiting. Unable to retrieve prefix {self.prefix}",
                "Prefix was not found in your Netbox instance.",
            )
            sys.exit(1)
        return self.prefix_object.id

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
    def _site_id(self):
        """
        Return the Netbox site ID associated with site.
        If the caller didn't set site, return None.
        """
        if self.site is not None:
            return site_id(self._netbox_obj, self.site)
        return None

    @property
    def status(self):
        """
        Return the status set by the caller.
        If the caller didn't set this, return None.
        """
        if "status" in self._info:
            return self._info["status"]
        return None

    @property
    def vlan(self):
        """
        Return the vlan by the caller.
        If the caller didn't set this, return None.
        """
        if "vlan" in self._info:
            return self._info["vlan"]
        return None

    @property
    def vlan_id(self):
        """
        Return the Netbox ID of the vlan set by the caller.
        If the caller didn't set vlan, return None.
        """
        if "vlan" in self._info:
            return vlan_vid_to_id(self._netbox_obj, self.vlan)
        return None
