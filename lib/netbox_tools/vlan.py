from netbox_tools.common import site_id, tag_id, vlan_group_id
from netbox_tools.common import create_slug, get_tag, get_tags

class Vlan(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['vid', 'vlan_name']
        self.optional_keys = ['description', 'group', 'role', 'site', 'status', 'tags'] # FYI only.  Not used in this class.

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('Vlan.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

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
            self.args['slug'] = create_slug(self.vlan_name)
            self.args['name'] = self.vlan_name
        if self.group != None:
            self.args['group'] = vlan_group_id(self.nb, self.group)
        if self.vid == None:
            print('Vlan.generate_args: Skipping. Missing mandatory parameter, vid.')
            return
        else:
            self.args['vid'] = self.vid
        if self.description != None:
            self.args['description'] = self.description
        if self.role != None:
            self.args['role'] = self.role
        if self.site != None:
            self.args['site'] = site_id(self.nb, self.site)
        if self.status != None:
            self.args['status'] = self.status
        if self.tags != None:
            self.args['tags'] = self.tags
        
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
            self.nb.ipam.vlans.create(self.args)
        except Exception as e:
            print('Vlan.create: Exiting. Unable to create Vlan {}.  Error was: {}'.format(self.vlan_name, e))
            exit(1)

    def update(self):
        print('Vlan.update: {}'.format(self.vlan_name))
        self.args['id'] = self.vlan_id
        try:
            self.vlan_object.update(self.args)
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
        if 'description' in self.info:
            return self.info['description']
        else:
            return None

    @property
    def group(self):
        if 'group' in self.info:
            return self.info['group']
        else:
            return None

    @property
    def role(self):
        if 'role' in self.info:
            return self.info['role']
        else:
            return None

    @property
    def site(self):
        if 'site' in self.info:
            return self.info['site']
        else:
            return None

    @property
    def status(self):
        if 'status' in self.info:
            return self.info['status']
        else:
            return None

    @property
    def vid(self):
        if 'vid' in self.info:
            return self.info['vid']
        else:
            return None

    @property
    def vlan_name(self):
        if 'vlan_name' in self.info:
            return self.info['vlan_name']
        else:
            return None

    @property
    def vlan_object(self):
        return self.nb.ipam.vlans.get(name=self.vlan_name)

    @property
    def vlan_id(self):
        return self.vlan_object.id

    @property
    def tags(self):
        if 'tags' in self.info:
            tag_list = list()
            for tag in self.info['tags']:
                tag_obj = get_tag(self.nb, tag)
                if tag_obj == None:
                    print('Vlan.tags: exiting. tag {} does not exist in netbox. Valid tags: {}'.format(tag, get_tags(self.nb)))
                    exit(1)
                tag_list.append(tag_id(self.nb, tag))
            return tag_list
        else:
            return None
