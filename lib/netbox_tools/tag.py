"""
Name: tag.py
Description: create, update, and delete operations on netbox tags
"""
from inspect import stack
import sys
from netbox_tools.colors import color_to_rgb
from netbox_tools.common import create_slug

OUR_VERSION = 101


class Tag:
    """
    create, update, and delete operations on netbox tags
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._mandatory_keys = set()
        self._mandatory_keys.add("name")
        self._optional_keys = set()  # Just FYI. Not used in this class.
        self._optional_keys.add("description")
        self._optional_keys.add("color")

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

    def _set_color(self):
        """
        Add color to args
        """
        if self.color is not None:
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

    def _generate_args(self):
        """
        Generate all supported arguments for create and update methods
        """
        self._set_color()
        self._set_description()
        self._set_name()
        self._set_slug()

    def delete(self):
        """
        delete a tag
        """
        if self.tag_obj is None:
            self.log(f"Nothing to do, tag {self.name} does not exist in netbox.")
            return
        self.log(f"{self.name}")
        try:
            self.tag_obj.delete()
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to delete tag {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create(self):
        """
        create a tag
        """
        self.log(f"{self.name}")
        try:
            self._netbox_obj.extras.tags.create(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to create tag {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def update(self):
        """
        update a tag
        """
        if self.tag_id is None:
            self.log(f"Skipping. tag {self.name} does not exist in Netbox")
            return
        self.log(f"{self.name}")
        self._args["id"] = self.tag_id
        try:
            self.tag_obj.update(self._args)
        except Exception as _general_exception:
            self.log(
                f"Exiting. Unable to update tag {self.name}.",
                f"Exception detail: {_general_exception}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into create and update methods
        """
        self._validate_keys()
        self._generate_args()
        if self.tag_obj is None:
            self.create()
        else:
            self.update()

    @property
    def color(self):
        """
        Return color set by the caller.
        """
        if "color" in self._info:
            return self._info["color"]
        return None

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
    def tag_obj(self):
        """
        Return tag object associated with name set by the caller.
        """
        return self._netbox_obj.extras.tags.get(name=self.name)

    @property
    def tag_id(self):
        """
        Return Netbox ID for the tag object associated with tag name set by the caller.
        """
        if self.tag_obj is not None:
            return self.tag_obj.id
        return None
