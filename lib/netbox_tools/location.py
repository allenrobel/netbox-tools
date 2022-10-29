'''
Name: location.py
Description: Class for create and update operations on netbox location
'''

from netbox_tools.common import create_slug
from netbox_tools.common import site_id

class Location(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys_create_update = ['name', 'site']

    def validate_keys_create_update(self):
        for key in self.mandatory_keys_create_update:
            if key not in self.info:
                print('Location.validate_keys_create_update: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args_create_update(self):
        self.args['name'] = self.info['name']
        self.args['site'] = site_id(self.nb, self.info['site'])
        self.args['slug'] = create_slug(self.info['name'])
        if 'tags' in self.info:
            self.args['tags'] = list()
            for tag in self.info['tags']:
                self.args['tags'].append(self.get_tag_id(tag))

    def delete(self):
        print('Location.delete: {}'.format(self.info['name']))
        try:
            self.location.delete()
        except Exception as e:
            print('Location.delete: WARNING. Unable to delete location {}.  Error was: {}'.format(self.info['name'], e))
            return

    def create(self):
        print('Location.create: {}'.format(self.info['name']))
        try:
            self.nb.dcim.locations.create(self.args)
        except Exception as e:
            print('Location.create: Exiting. Unable to create location {}.  Error was: {}'.format(self.info['name'], e))
            exit(1)

    def update(self):
        print('Location.update: {}'.format(self.info['name']))
        self.args['id'] = self.location_id
        try:
            self.location.update(self.args)
        except Exception as e:
            print('Location.update: Exiting. Unable to update location {}.  Error was: {}'.format(self.info['name'], e))
            exit(1)

    def create_or_update(self):
        self.validate_keys_create_update()
        self.generate_args_create_update()
        if self.location == None:
            self.create()
        else:
            self.update()

    @property
    def location(self):
        return self.nb.dcim.locations.get(name=self.info['name'])

    @property
    def location_id(self):
        return self.location.id
