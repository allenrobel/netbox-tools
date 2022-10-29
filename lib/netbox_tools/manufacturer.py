'''
Name: manufacturer.py
Description: Class for create and update operations on netbox manufacturer
'''

from netbox_tools.common import create_slug

class Manufacturer(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_create_update_keys = ['name']
        self.mandatory_delete_keys = ['name']
        self.optional_keys = []

    def validate_delete_keys(self):
        for key in self.mandatory_delete_keys:
            if key not in self.info:
                print('manufacturer.validate_delete_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def validate_create_update_keys(self):
        for key in self.mandatory_create_update_keys:
            if key not in self.info:
                print('manufacturer.validate_create_update_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_create_update_args(self):
        self.args['name'] = self.name
        self.args['slug'] = create_slug(self.name)
        for key in self.optional_keys:
            if key in self.info:
                self.args[key] = self.info[key]

    def delete(self):
        self.validate_delete_keys()
        if self.manufacturer == None:
            print('Manufacturer.delete: Nothing to do. Manufacturer {} does not exist in netbox.'.format(self.name))
            return
        print('Manufacturer.delete: {}'.format(self.name))
        try:
            self.manufacturer.delete()
        except Exception as e:
            print('Manufacturer.delete: Error. Unable to delete manufacturer {}.  Error was: {}'.format(self.name, e))
            return

    def create(self):
        print('Manufacturer.create: {}'.format(self.name))
        try:
            self.nb.dcim.manufacturers.create(self.args)
        except Exception as e:
            print('manufacturer.create: Exiting. Unable to create manufacturer {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def update(self):
        print('Manufacturer.update: {}'.format(self.name))
        self.args['id'] = self.manufacturer_id
        try:
            self.manufacturer.update(self.args)
        except Exception as e:
            print('manufacturer.update: Exiting. Unable to update manufacturer {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def create_or_update(self):
        self.validate_create_update_keys()
        self.generate_create_update_args()
        if self.manufacturer == None:
            self.create()
        else:
            self.update()

    @property
    def name(self):
        return self.info['name']

    @property
    def manufacturer(self):
        return self.nb.dcim.manufacturers.get(name=self.name)

    @property
    def manufacturer_id(self):
        return self.manufacturer.id

