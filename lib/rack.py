'''
Name: rack.py
Description: Class for create and update operations on netbox rack
'''

from lib.common import create_slug
from lib.common import site_id
from lib.common import location_id

class Rack(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['name', 'site', 'location']
        self.optional_keys = ['u_height']
        self.validate_keys()
        self.generate_args()

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('Rack.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['name'] = self.name
        self.args['location'] = location_id(self.nb, self.location)
        self.args['site'] = site_id(self.nb, self.site)
        for key in self.optional_keys:
            if key in self.info:
                self.args[key] = self.info[key]

    def create(self):
        print('Rack.create: {}'.format(self.name))
        try:
            self.nb.dcim.racks.create(self.args)
        except Exception as e:
            print('Rack.create: Exiting. Unable to create rack {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def update(self):
        print('Rack.update: {}'.format(self.name))
        self.args['id'] = self.rack_id
        try:
            self.rack.update(self.args)
        except Exception as e:
            print('Rack.update: Exiting. Unable to update rack {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def create_or_update(self):
        if self.rack == None:
            self.create()
        else:
            self.update()

    @property
    def name(self):
        return self.info['name']

    @property
    def location(self):
        return self.info['location']

    @property
    def rack(self):
        return self.nb.dcim.racks.get(name=self.info['name'])

    @property
    def rack_id(self):
        return self.rack.id

    @property
    def site(self):
        return self.info['site']
