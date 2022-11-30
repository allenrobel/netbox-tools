"""
Name: manufacturer.py
Description: create, update, and delete operations on netbox manufacturer
"""

from inspect import stack
import sys
from netbox_tools.common import create_slug


class Manufacturer:
    """
    create, update, and delete operations on netbox manufacturer
    """

    def __init__(self, netbox_obj, info):
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_create_update_keys = set()
        self._mandatory_create_update_keys.add("name")
        self._mandatory_delete_keys = set()
        self._mandatory_delete_keys.add("name")
        self._optional_keys = set()

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
                self.log(
                    f"exiting. mandatory key {key} not found in info {self._info}"
                )
                sys.exit(1)

    def _validate_create_update_keys(self):
        """
        Verify that all mandatory create/update operation keys are set.
        If all keys are not set, log an error and exit.
        """
        for key in self._mandatory_create_update_keys:
            if key not in self._info:
                self.log(
                    f"exiting. mandatory key {key} not found in info {self._info}"
                )
                sys.exit(1)

    def _generate_create_update_args(self):
        """
        Generate all supported arguments for create and update methods
        """
        self._args["name"] = self.name
        self._args["slug"] = create_slug(self.name)
        for key in self._optional_keys:
            if key in self._info:
                self._args[key] = self._info[key]

    def delete(self):
        """
        delete a manufacturer
        """
        self._validate_delete_keys()
        if self.manufacturer_obj == None:
            self.log(
                f"Nothing to do. Manufacturer {self.name} does not exist in netbox."
            )
            return
        self.log(f"{self.name}")
        try:
            self.manufacturer_obj.delete()
        except Exception as _general_exception:
            self.log(
                f"Error. Unable to delete manufacturer {self.name}",
                f"Exception detail: {_general_exception}",
            )
            return

    def create(self):
        """
        create a manufacturer
        """
        self.log(f"{self.name}")
        try:
            self._netbox_obj.dcim.manufacturers.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"Error. Unable to create manufacturer {self.name}",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update a manufacturer
        """
        self.log(f"{self.name}")
        self._args["id"] = self.manufacturer_id
        try:
            self.manufacturer_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"Error. Unable to update manufacturer {self.name}",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_create_update_keys()
        self._generate_create_update_args()
        if self.manufacturer_obj == None:
            self.create()
        else:
            self.update()

    @property
    def name(self):
        """
        Return the manufacturer name set by the caller.
        """
        return self._info["name"]

    @property
    def manufacturer_obj(self):
        """
        Return the manufacturer object associated with the
        manufacturer name set by the caller.
        Netbox will return None if this does not exist.
        """
        return self._netbox_obj.dcim.manufacturers.get(name=self.name)

    @property
    def manufacturer_id(self):
        """
        Return the Netbox ID of the manufacturer object associated
        with the manufacturer name set by the caller.
        Return None if the manufacturer object does not exist in Netbox.
        """
        if self.manufacturer_obj is not None:
            return self.manufacturer_obj.id
        return None
