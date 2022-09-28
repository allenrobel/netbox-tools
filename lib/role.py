'''
Name: role.py
Description: Class for create and update operations on netbox device roles
'''

from lib.common import create_slug
from lib.colors import color_to_rgb

class Role(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['color', 'name']
        self.optional_keys = ['description']

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('Role.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['name'] = self.name
        self.args['color'] = self.rgb
        self.args['slug'] = create_slug(self.name)
        for key in self.optional_keys:
            if key in self.info:
                self.args[key] = self.info[key]

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

# # device role

# def get_device_role_args(info):
#     mandatory_keys = ['color', 'name']
#     for key in mandatory_keys:
#         if key not in info:
#             print('get_device_role_args: exiting. mandatory key {} not found in info {}'.format(key, info))
#             exit(1)
#     args = dict()
#     args['color'] = color_to_rgb(info['color'])
#     if 'description' in info:
#         args['description'] = info['description']
#     args['name'] = info['name']
#     args['slug'] = create_slug(info['name'])
#     return args

# def update_device_role(info, role):
#     print('update_device_role: {}'.format(info['name']))
#     args = get_device_role_args(info)
#     # print(dict(role))
#     role.update(args)

# def create_device_role(info):
#     print('create_device_role: {}'.format(info['name']))
#     args = get_device_role_args(info)
#     nb.dcim.device_roles.create(args)

# def create_or_update_device_role(info):
#     role = nb.dcim.device_roles.get(name=info['name'])
#     if role == None:
#         create_device_role(info)
#     else:
#         update_device_role(info, role)
