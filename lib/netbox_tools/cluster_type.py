"""
Name: cluster_type.py
Description: Class for create and update operations on netbox cluster_type
"""
import sys
from inspect import stack
from netbox_tools.common import create_slug, tag_id

OUR_VERSION = 103


class ClusterType:
    """
    create, update, and delete operations on netbox virtualization.cluster_types
    """

    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = {}
        self._populate_mandatory_keys()
        self._populate_optional_keys()

    def _populate_mandatory_keys(self):
        """
        The mandatory keys netbox expects to be present.  These are
        checked in self._validate_keys_create_update()
        """
        self._mandatory_keys_create_update = set()
        self._mandatory_keys_create_update.add("name")

    def _populate_optional_keys(self):
        """
        self._optional_keys are not used, currently.  They're just FYI.
        """
        self._optional_keys = set()
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
        verify that all mandatory keys are present
        """
        for key in self._mandatory_keys_create_update:
            if key not in self._info:
                self.log(
                    f"exiting. mandatory key {key} not found in info {self._info}"
                )
                sys.exit(1)

    def _set_description(self):
        """
        populate args with the cluster_type description
        """
        if self.description is not None:
            self._args["description"] = self.description

    def _set_name(self):
        """
        populate args with the cluster_type name
        """
        self._args["name"] = self.name

    def _set_slug(self):
        """
        populate args with a url-friendly name for the cluster_type
        If the caller has not set the slug, we do it here
        """
        if self.slug is None:
            self._args["slug"] = create_slug(self.name)
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

    def _generate_args_create_update(self):
        """
        generate all supported arguments
        """
        self._set_description()
        self._set_name()
        self._set_slug()
        self._set_tags()

    def delete(self):
        """
        delete a cluster_type
        """
        self.log(f"{self._info['name']}")
        try:
            self.cluster_type_object.delete()
        except Exception as _general_error:
            self.log(
                f"WARNING. Unable to delete cluster_type {self._info['name']}.",
                f"Exception detail: {_general_error}",
                "continuing nonetheless..."
            )
            return

    def create(self):
        """
        create a cluster_type
        """
        self.log(f"{self._info['name']}")
        try:
            self._netbox_obj.virtualization.cluster_types.create(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to create cluster_type {self._info['name']}",
                f"Exception detail: {_general_error}"
            )
            sys.exit(1)

    def update(self):
        """
        update a cluster_type
        """
        self.log("{}".format(self._info["name"]))
        try:
            self.cluster_type_object.update(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to update cluster_type {self._info['name']}",
                f"Exception detail: {_general_error}"
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into creation and updation methods
        """
        self._validate_keys_create_update()
        self._generate_args_create_update()
        if self.cluster_type_object is None:
            self.create()
        else:
            self.update()

    @property
    def cluster_type_object(self):
        """
        retrieve a cluster_type object from netbox by filtering on self.name and return it
        """
        return self._netbox_obj.virtualization.cluster_types.get(name=self.name)

    @property
    def cluster_type_id(self):
        """
        return the netbox ID of a cluster_type object
        """
        return self.cluster_type_object.id

    @property
    def description(self):
        """
        set the description of the cluster_type
        """
        if "description" in self._info:
            return self._info["description"]
        return None

    @property
    def name(self):
        """
        set the name of the cluster_type. Used to check if the cluster_type
        already exists, and for the name of new cluster_types
        """
        if "name" in self._info:
            return self._info["name"]
        return None

    @property
    def slug(self):
        """
        set the slug (url friendly name) of the cluster_type.  If this
        is not set by the caller, we set it in self._set_slug()
        """
        if "slug" in self._info:
            return self._info["slug"]
        return None

    @property
    def tags(self):
        """
        set the cluster_type's tags
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
