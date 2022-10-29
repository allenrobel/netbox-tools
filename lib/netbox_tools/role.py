'''
Name: role.py
Description: Class for create and update operations on netbox device roles
'''

from netbox_tools.common import create_slug, get_tag, get_tags, tag_id
from netbox_tools.colors import color_to_rgb

class Role(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['color', 'name']
        self.optional_keys = ['description', 'tags,'] # FYI only.  Not used in this class.

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('Role.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['name'] = self.name
        self.args['color'] = self.rgb
        self.args['slug'] = create_slug(self.name)
        if self.description != None:
            self.args['description'] = self.description
        if self.tags != None:
            self.args['tags'] = self.tags

    def delete(self):
        if self.role == None:
            print('Role.delete: Nothing to do. Role {} does not exist in netbox.'.format(self.name))
            return
        print('Role.delete: {}'.format(self.name))
        try:
            self.role.delete()
        except Exception as e:
            print('Role.delete: Error. Unable to delete role {}.  Error was: {}'.format(self.name, e))
            return

    def create(self):
        print('Role.create: {}'.format(self.name))
        try:
            self.nb.dcim.device_roles.create(self.args)
        except Exception as e:
            print('Role.create: Exiting. Unable to create role {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def update(self):
        print('Role.update: {}'.format(self.name))
        self.args['id'] = self.role_id
        try:
            self.role.update(self.args)
        except Exception as e:
            print('Role.update: Exiting. Unable to update role {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def create_or_update(self):
        self.validate_keys()
        self.generate_args()
        if self.role == None:
            self.create()
        else:
            self.update()

    @property
    def color(self):
        return self.info['color']

    @property
    def description(self):
        if 'description' in self.info:
            return self.info['description']
        else:
            return None

    @property
    def name(self):
        return self.info['name']

    @property
    def rgb(self):
        return color_to_rgb(self.info['color'])

    @property
    def role(self):
        return self.nb.dcim.device_roles.get(name=self.name)

    @property
    def role_id(self):
        return self.role.id

    @property
    def slug(self):
        return create_slug(self.name)

    @property
    def tags(self):
        if 'tags' in self.info:
            tag_list = list()
            for tag in self.info['tags']:
                tag_obj = get_tag(self.nb, tag)
                if tag_obj == None:
                    print('DeviceType.tags: exiting. tag {} does not exist in netbox. Valid tags: {}'.format(tag, get_tags(self.nb)))
                    exit(1)
                tag_list.append(tag_id(self.nb, tag))
            return tag_list
        else:
            return None
