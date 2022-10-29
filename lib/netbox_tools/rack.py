'''
Name: rack.py
Description: Class for create and update operations on netbox rack
'''

from netbox_tools.common import create_slug, get_tag, get_tags, location_id, site_id, tag_id

class Rack(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_delete_keys = ['name']
        self.mandatory_create_update_keys = ['name', 'site', 'location']
        self.optional_keys = ['u_height', 'comments'] # these are FYI only i.e. not used in this class

    def validate_delete_keys(self):
        for key in self.mandatory_delete_keys:
            if key not in self.info:
                print('Rack.validate_delete_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)
    def validate_create_update_keys(self):
        for key in self.mandatory_create_update_keys:
            if key not in self.info:
                print('Rack.validate_delete_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_create_update_args(self):
        self.args['name'] = self.name
        self.args['location'] = location_id(self.nb, self.location)
        self.args['site'] = site_id(self.nb, self.site)
        if self.u_height != None:
            self.args['u_height'] = self.u_height
        if self.comments != None:
            self.args['comments'] = self.comments
        if self.tags != None:
            self.args['tags'] = self.tags

    def delete(self):
        self.validate_delete_keys()
        if self.rack == None:
            print('Rack.delete: Nothing to do. Rack {} does not exist in netbox.'.format(self.name))
            return
        print('Rack.delete: {}'.format(self.name))
        try:
            self.rack.delete()
        except Exception as e:
            print('Rack.delete: Error. Unable to delete rack {}.  Error was: {}'.format(self.name, e))
            return

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
        self.validate_create_update_keys()
        self.generate_create_update_args()
        if self.rack == None:
            self.create()
        else:
            self.update()

    @property
    def comments(self):
        if 'comments' in self.info:
            return self.info['comments']
        else:
            return None

    @property
    def name(self):
        return self.info['name']

    @property
    def location(self):
        return self.info['location']

    @property
    def rack(self):
        return self.nb.dcim.racks.get(name=self.name)

    @property
    def rack_id(self):
        return self.rack.id

    @property
    def site(self):
        return self.info['site']

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

    @property
    def u_height(self):
        if 'u_height' in self.info:
            return self.info['u_height']
        else:
            return None
