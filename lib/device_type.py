from lib.common import create_slug
from lib.common import manufacturer_id
from lib.common import get_tag, get_tags, tag_id

class DeviceType(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_create_update_keys = ['manufacturer', 'model']
        self.mandatory_delete_keys = ['model']
        self.optional_keys = ['comments', 'tags'] # this is FYI only and is not used below

    def validate_delete_keys(self):
        for key in self.mandatory_delete_keys:
            if key not in self.info:
                print('DeviceType.validate_delete_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)
    def validate_create_update_keys(self):
        for key in self.mandatory_create_update_keys:
            if key not in self.info:
                print('DeviceType.validate_create_update_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_create_update_args(self):
        self.args['manufacturer'] = manufacturer_id(self.nb, self.manufacturer)
        self.args['model'] = self.model
        self.args['slug'] = self.slug
        if self.comments != None:
            self.args['comments'] = self.comments
        if self.tags != None:
            self.args['tags'] = self.tags

    def delete(self):
        self.validate_delete_keys()
        if self.device_type == None:
            print('DeviceType.delete: Nothing to do. device_type {} does not exist in netbox.'.format(self.model))
            return
        print('DeviceType.delete: {}'.format(self.model))
        try:
            self.device_type.delete()
        except Exception as e:
            print('DeviceType.delete: WARNING. Unable to delete device_type {}.  Error was: {}'.format(self.model, e))
            return

    def create(self):
        print('DeviceType.create: {}'.format(self.model))
        try:
            self.nb.dcim.device_types.create(self.args)
        except Exception as e:
            print('DeviceType.create: Exiting. Unable to create device_type {}.  Error was: {}'.format(self.model, e))
            exit(1)

    def update(self):
        print('DeviceType.update: {}'.format(self.model))
        self.args['id'] = self.device_type_id
        try:
            self.device_type.update(self.args)
        except Exception as e:
            print('DeviceType.update: Exiting. Unable to update device_type {}.  Error was: {}'.format(self.model, e))
            exit(1)

    def create_or_update(self):
        self.validate_create_update_keys()
        self.generate_create_update_args()
        if self.device_type == None:
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
    def manufacturer(self):
        return self.info['manufacturer']

    @property
    def model(self):
        return self.info['model']

    @property
    def slug(self):
        return self.model.lower()

    @property
    def device_type(self):
        return self.nb.dcim.device_types.get(slug=self.model.lower())

    @property
    def device_type_id(self):
        return self.device_type.id

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
