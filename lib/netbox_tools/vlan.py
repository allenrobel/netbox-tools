from netbox_tools.common import site_id, tag_id, vlan_group_id
from netbox_tools.common import create_slug, get_tag, get_tags

class Vlan(object):
    def __init__(self, netbox_obj, info):
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = dict()
        self.mandatory_keys = ['vid', 'vlan_name']
        self.optional_keys = ['description', 'group', 'role', 'site', 'status', 'tags'] # FYI only.  Not used in this class.

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self._info:
                print('Vlan.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self._info))
                exit(1)

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

    def generate_args(self):
        if self.site != None and self.group != None:
            print('Vlan.generate_args: Skipping {}. site and group are mutually-exclusive. Got group {}, site {}'.format(
                self.vlan_name,
                self.group,
                self.site
            ))
            return
        if self.vlan_name == None:
            print('Vlan.generate_args: Skipping. vlan_name is a mandatory parameter, but is missing.')
            return
        else:
            self._args['slug'] = create_slug(self.vlan_name)
            self._args['name'] = self.vlan_name
        if self.group != None:
            self._args['group'] = vlan_group_id(self._netbox_obj, self.group)
        if self.vid == None:
            print('Vlan.generate_args: Skipping. Missing mandatory parameter, vid.')
            return
        else:
            self._args['vid'] = self.vid
        if self.description != None:
            self._args['description'] = self.description
        if self.role != None:
            self._args['role'] = self.role
        if self.site != None:
            self._args['site'] = site_id(self._netbox_obj, self.site)
        if self.status != None:
            self._args['status'] = self.status
        self._set_tags()
        
    def delete(self):
        print('Vlan.delete: {}'.format(self.vlan_name))
        if self.vlan_object == None:
            print('Vlan.delete: Nothing to do. Vlan {} does not exist in netbox.'.format(self.vlan_name))
            return
        try:
            self.vlan_object.delete()
        except Exception as e:
            print('Vlan.delete: WARNING. Unable to delete Vlan {}.  Error was: {}'.format(self.vlan_name, e))
            return

    def create(self):
        print('Vlan.create: {}'.format(self.vlan_name))
        try:
            self._netbox_obj.ipam.vlans.create(self._args)
        except Exception as e:
            print('Vlan.create: Exiting. Unable to create Vlan {}.  Error was: {}'.format(self.vlan_name, e))
            exit(1)

    def update(self):
        print('Vlan.update: {}'.format(self.vlan_name))
        self._args['id'] = self.vlan_id
        try:
            self.vlan_object.update(self._args)
        except Exception as e:
            print('Vlan.update: Exiting. Unable to update Vlan {}.  Error was: {}'.format(self.vlan_name, e))
            exit(1)

    def create_or_update(self):
        self.validate_keys()
        self.generate_args()
        if self.vlan_object == None:
            self.create()
        else:
            self.update()

    @property
    def description(self):
        if 'description' in self._info:
            return self._info['description']
        else:
            return None

    @property
    def group(self):
        if 'group' in self._info:
            return self._info['group']
        else:
            return None

    @property
    def role(self):
        if 'role' in self._info:
            return self._info['role']
        else:
            return None

    @property
    def site(self):
        if 'site' in self._info:
            return self._info['site']
        else:
            return None

    @property
    def status(self):
        if 'status' in self._info:
            return self._info['status']
        else:
            return None

    @property
    def vid(self):
        if 'vid' in self._info:
            return self._info['vid']
        else:
            return None

    @property
    def vlan_name(self):
        if 'vlan_name' in self._info:
            return self._info['vlan_name']
        else:
            return None

    @property
    def vlan_object(self):
        return self._netbox_obj.ipam.vlans.get(name=self.vlan_name)

    @property
    def vlan_id(self):
        return self.vlan_object.id

    @property
    def tags(self):
        """
        Return the list of tag names set by the caller.
        If the caller didn't set this, return None.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None
