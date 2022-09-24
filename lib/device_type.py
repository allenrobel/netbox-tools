from lib.common import create_slug
from lib.common import manufacturer_id

class DeviceType(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['manufacturer', 'model']
        self.optional_keys = ['comments']
        self.validate_keys()
        self.generate_args()

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('DeviceType.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['manufacturer'] = manufacturer_id(self.nb, self.manufacturer)
        self.args['model'] = self.model
        self.args['slug'] = self.slug
        for key in self.optional_keys:
            if key in self.info:
                self.args[key] = self.info[key]

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
        if self.device_type == None:
            self.create()
        else:
            self.update()

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

