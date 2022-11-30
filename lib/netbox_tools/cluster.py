"""
Name: cluster.py
Description: Class for create and update operations on netbox cluster
"""
import sys
from inspect import stack
from netbox_tools.common import create_slug
from netbox_tools.common import cluster_group_id, cluster_type_id, site_id, tag_id

OUR_VERSION = 103


class Cluster:
    """
    create, update, delete operations on netbox endpoint: virtualization.clusters
    """

    def __init__(self, netbox_obj, info):
        self._netbox_obj = netbox_obj
        self._info = info
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._args = {}
        self._populate_mandatory_keys()
        self._populate_mutex_keys()

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self._classname}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _populate_mutex_keys(self):
        """
        Netbox considers the keys in this dictionary to be mutually-exclusive.
        We validate this in self._test_mutex()
        """
        self.mutex_keys = set()
        self.mutex_keys.add("site")
        self.mutex_keys.add("group")

    def _populate_mandatory_keys(self):
        """
        The mandatory keys netbox expects to be present.
        These are checked in self._validate_keys_create_update()
        """
        self.mandatory_keys_create_update = set()
        self.mandatory_keys_create_update.add("cluster")
        self.mandatory_keys_create_update.add("type")

    def _validate_keys_create_update(self):
        """
        verify that all mandatory keys are present
        """
        for key in self.mandatory_keys_create_update:
            if key not in self._info:
                self.log(f"exiting. mandatory key {key} not found in info {self._info}")
                sys.exit(1)

    def _test_mutex(self, test_key):
        """
        verify that the user has not populated more than one of the mutex keys
        """
        if test_key not in self._info:
            return
        if self._info[test_key] is None:
            return
        for key in self.mutex_keys:
            if key == test_key:
                continue
            if key not in self._info:
                continue
            if self._info[key] is not None:
                self.log(
                    f"exiting. {test_key} is set and is mutually-exclusive to {key}.",
                    f"Unset {test_key} or {key} and try again.",
                )
                sys.exit(1)

    def _set_group(self):
        """
        validate and set the cluster's group, if any; converting it to a netbox id
        """
        self._test_mutex("group")
        if self.group is not None:
            self._args["group"] = cluster_group_id(self._netbox_obj, self._info["group"])

    def _set_name(self):
        """
        set the cluster's name
        """
        self._args["name"] = self._info["cluster"]

    def _set_site(self):
        """
        set the cluster's site, if any; converting it to a netbox id
        """
        self._test_mutex("site")
        if self.site is not None:
            self._args["site"] = site_id(self._netbox_obj, self.site)

    def _set_slug(self):
        """
        populate args with a url-friendly name for the cluster_type
        If the caller has not set the slug, we do it here
        """
        if self.slug is None:
            self._args["slug"] = create_slug(self.cluster)
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

    def _set_type(self):
        """
        set the cluster's type, converting it to a netbox id
        """
        self._args["type"] = cluster_type_id(self._netbox_obj, self.type)

    def _generate_args_create_update(self):
        """
        generate all supported arguments
        """
        self._set_group()
        self._set_name()
        self._set_site()
        self._set_slug()
        self._set_tags()
        self._set_type()

    def delete(self):
        """
        delete a cluster
        """
        self.log(f"{self._info['name']}")
        try:
            self.cluster_object.delete()
        except Exception as _general_error:
            self.log(
                f"WARNING. Unable to delete cluster {self._info['name']}.",
                f"Exception detail: {_general_error}",
            )
            return

    def create(self):
        """
        create a cluster
        """
        self.log(f"{self._info['cluster']}")
        try:
            self._netbox_obj.virtualization.clusters.create(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to create cluster {self._info['cluster']}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def update(self):
        """
        update a cluster
        """
        self.log(f"{self._info['cluster']}")
        self._args["id"] = self.cluster_id
        try:
            self.cluster_object.update(self._args)
        except Exception as _general_error:
            self.log(
                f"exiting. Unable to update cluster {self._info['cluster']}.",
                f"Exception detail: {_general_error}",
            )
            sys.exit(1)

    def create_or_update(self):
        """
        entry point into creation and updation methods
        """
        self._validate_keys_create_update()
        self._generate_args_create_update()
        if self.cluster_object is None:
            self.create()
        else:
            self.update()

    @property
    def cluster(self):
        """
        set the name of the cluster. Used to check if the cluster
        already exists, and for the name of new clusters
        """
        if "cluster" in self._info:
            return self._info["cluster"]
        return None

    @property
    def cluster_object(self):
        """
        retrieve a cluster object from netbox by filtering on self.cluster and return it
        """
        return self._netbox_obj.virtualization.clusters.get(name=self.cluster)

    @property
    def cluster_id(self):
        """
        return the netbox ID of a cluster object
        """
        return self.cluster_object.id

    @property
    def group(self):
        """
        return the cluster's group, if any, or None if the cluster's group is not set.
        """
        if "group" in self._info:
            return self._info["group"]
        return None

    @property
    def site(self):
        """
        return the cluster's site, if any, or None if the cluster's site is not set.
        """
        if "site" in self._info:
            return self._info["site"]
        return None

    @property
    def slug(self):
        """
        set the netbox slug (url friendly name) of the cluster.  If this
        is not set by the caller, we set it in self._set_slug()
        """
        if "slug" in self._info:
            return self._info["slug"]
        return None

    @property
    def tags(self):
        """
        set the cluster's tags
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None

    @property
    def type(self):
        """
        return the cluster's type, if any, or None if the cluster's type is not set.
        """
        if "type" in self._info:
            return self._info["type"]
        return None
