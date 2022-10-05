from lib.common import tag_id
from lib.common import create_slug, get_tag, get_tags

class VlanGroup(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['vlan_group']
        self.optional_keys = ['description', 'max_vid', 'min_vid', 'tags'] # FYI only.  Not used in this class.

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('VlanGroup.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['name'] = self.vlan_group_name
        self.args['slug'] = create_slug(self.vlan_group_name)
        if self.description != None:
            self.args['description'] = self.description
        if self.tags != None:
            self.args['tags'] = self.tags
        if self.max_vid != None:
            self.args['max_vid'] = self.max_vid
        if self.min_vid != None:
            self.args['min_vid'] = self.min_vid
        
    def delete(self):
        print('VlanGroup.delete: {}'.format(self.vlan_group_name))
        if self.vlan_group_object == None:
            print('VlanGroup.delete: Nothing to do. VlanGroup {} does not exist in netbox.'.format(self.vlan_group_name))
            return
        try:
            self.vlan_group_object.delete()
        except Exception as e:
            print('VlanGroup.delete: WARNING. Unable to delete VlanGroup {}.  Error was: {}'.format(self.vlan_group_name, e))
            return

    def create(self):
        print('VlanGroup.create: {}'.format(self.vlan_group_name))
        try:
            self.nb.ipam.vlan_groups.create(self.args)
        except Exception as e:
            print('VlanGroup.create: Exiting. Unable to create VlanGroup {}.  Error was: {}'.format(self.vlan_group_name, e))
            exit(1)

    def update(self):
        print('VlanGroup.update: {}'.format(self.vlan_group_name))
        self.args['id'] = self.vlan_group_id
        try:
            self.vlan_group_object.update(self.args)
        except Exception as e:
            print('VlanGroup.update: Exiting. Unable to update VlanGroup {}.  Error was: {}'.format(self.vlan_group_name, e))
            exit(1)

    def create_or_update(self):
        self.validate_keys()
        self.generate_args()
        if self.vlan_group_object == None:
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
    def vlan_group_object(self):
        return self.nb.ipam.vlan_groups.get(name=self.vlan_group_name)

    @property
    def vlan_group_id(self):
        return self.vlan_group_object.id

    @property
    def tags(self):
        if 'tags' in self.info:
            tag_list = list()
            for tag in self.info['tags']:
                tag_obj = get_tag(self.nb, tag)
                if tag_obj == None:
                    print('VlanGroup.tags: exiting. tag {} does not exist in netbox. Valid tags: {}'.format(tag, get_tags(self.nb)))
                    exit(1)
                tag_list.append(tag_id(self.nb, tag))
            return tag_list
        else:
            return None
