from lib.colors import color_to_rgb
from lib.common import create_slug

class Tag(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['color', 'name']
        self.optional_keys = ['description']

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('Tag.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['name'] = self.name
        self.args['color'] = self.rgb
        self.args['slug'] = create_slug(self.name)
        for key in self.optional_keys:
            if key in self.info:
                self.args[key] = self.info[key]

    def delete(self):
        if self.tag == None:
            print('exiting. Tag {} does not exist in netbox.'.format(self.name))
            exit(1)
        print('Tag.delete: {}'.format(self.name))
        try:
            self.tag.delete()
        except Exception as e:
            print('Tag.delete: Exiting. Unable to delete tag {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def create(self):
        print('Tag.create: {}'.format(self.name))
        try:
            self.nb.extras.tags.create(self.args)
        except Exception as e:
            print('Tag.create: Exiting. Unable to create tag {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def update(self):
        print('Tag.update: {}'.format(self.name))
        self.args['id'] = self.tag_id
        try:
            self.tag.update(self.args)
        except Exception as e:
            print('Tag.update: Exiting. Unable to update tag {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def create_or_update(self):
        self.validate_keys()
        self.generate_args()
        if self.tag == None:
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
    def tag(self):
        return self.nb.extras.tags.get(name=self.name)

    @property
    def tag_id(self):
        return self.tag.id
