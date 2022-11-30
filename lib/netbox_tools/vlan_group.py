from netbox_tools.common import tag_id
from netbox_tools.common import create_slug

OUR_VERSION = 101

class VlanGroup(object):
    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['vlan_group']
        self.optional_keys = ['description', 'max_vid', 'min_vid', 'tags'] # FYI only.  Not used in this class.

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('VlanGroup.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def _set_tags(self):
        """
        Add tags, if any, to args; converting them to netbox IDs
        """
        if self.tags is None:
            return
        self.args["tags"] = []
        for tag in self.tags:
            tid = tag_id(self._netbox_obj, tag)
            if tid is None:
                self.log(f"tag {tag} not found in Netbox.  Skipping.")
                continue
            self.args["tags"].append(tid)

    def generate_args(self):
        self.args['name'] = self.vlan_group_name
        self.args['slug'] = create_slug(self.vlan_group_name)
        if self.description != None:
            self.args['description'] = self.description
        self._set_tags()
        if self.max_vid != None:
            self.args['max_vid'] = self.max_vid
        if self.min_vid != None:
            self.args['min_vid'] = self.min_vid
        
    def delete(self):
        print('VlanGroup.delete: {}'.format(self.vlan_group_name))
        if self.vlan_group_obj == None:
            print('VlanGroup.delete: Nothing to do. VlanGroup {} does not exist in netbox.'.format(self.vlan_group_name))
            return
        try:
            self.vlan_group_obj.delete()
        except Exception as e:
            print('VlanGroup.delete: WARNING. Unable to delete VlanGroup {}.  Error was: {}'.format(self.vlan_group_name, e))
            return

    def create(self):
        print('VlanGroup.create: {}'.format(self.vlan_group_name))
        try:
            self._netbox_obj.ipam.vlan_groups.create(self.args)
        except Exception as e:
            print('VlanGroup.create: Exiting. Unable to create VlanGroup {}.  Error was: {}'.format(self.vlan_group_name, e))
            exit(1)

    def update(self):
        print('VlanGroup.update: {}'.format(self.vlan_group_name))
        self.args['id'] = self.vlan_group_id
        try:
            self.vlan_group_obj.update(self.args)
        except Exception as e:
            print('VlanGroup.update: Exiting. Unable to update VlanGroup {}.  Error was: {}'.format(self.vlan_group_name, e))
            exit(1)

    def create_or_update(self):
        self.validate_keys()
        self.generate_args()
        if self.vlan_group_obj == None:
            self.create()
        else:
            self.update()

    @property
    def max_vid(self):
        if 'max_vid' in self.info:
            return self.info['max_vid']
        else:
            return None

    @property
    def min_vid(self):
        if 'min_vid' in self.info:
            return self.info['min_vid']
        else:
            return None

    @property
    def vlan_group_name(self):
        return self.info['vlan_group']

    @property
    def description(self):
        if 'description' in self.info:
            return self.info['description']
        else:
            return None

    @property
    def vlan_group_obj(self):
        return self._netbox_obj.ipam.vlan_groups.get(name=self.vlan_group_name)

    @property
    def vlan_group_id(self):
        return self.vlan_group_obj.id

    @property
    def tags(self):
        """
        Return the list of tag names set by the caller.
        If the caller didn't set this, return None.
        """
        if "tags" in self.info:
            return self.info["tags"]
        return None
