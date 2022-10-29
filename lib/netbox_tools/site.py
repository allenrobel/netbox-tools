from netbox_tools.common import tag_id
from netbox_tools.common import create_slug, get_tag, get_tags

class Site(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['name']
        self.optional_keys = ['description', 'tags'] # FYI only.  Not used in this class.

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('Site.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['name'] = self.name
        self.args['slug'] = create_slug(self.name)
        if self.description != None:
            self.args['description'] = self.description
        if self.tags != None:
            self.args['tags'] = self.tags
        
    def delete(self):
        print('Site.delete: {}'.format(self.name))
        if self.site == None:
            print('Site.delete: Nothing to do. Site {} does not exist in netbox.'.format(self.name))
            return
        try:
            self.site.delete()
        except Exception as e:
            print('Site.delete: WARNING. Unable to delete site {}.  Error was: {}'.format(self.name, e))
            return

    def create(self):
        print('Site.create: {}'.format(self.name))
        try:
            self.nb.dcim.sites.create(self.args)
        except Exception as e:
            print('Site.create: Exiting. Unable to create site {}.  Error was: {}'.format(self.site, e))
            exit(1)

    def update(self):
        print('Site.update: {}'.format(self.site))
        self.args['id'] = self.site_id
        try:
            self.site.update(self.args)
        except Exception as e:
            print('Site.update: Exiting. Unable to update site {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def create_or_update(self):
        self.validate_keys()
        self.generate_args()
        if self.site == None:
            self.create()
        else:
            self.update()

    @property
    def name(self):
        return self.info['name']

    @property
    def description(self):
        if 'description' in self.info:
            return self.info['description']
        else:
            return None

    @property
    def site(self):
        return self.nb.dcim.sites.get(name=self.name)

    @property
    def site_id(self):
        return self.site.id

    @property
    def tags(self):
        if 'tags' in self.info:
            tag_list = list()
            for tag in self.info['tags']:
                tag_obj = get_tag(self.nb, tag)
                if tag_obj == None:
                    print('Site.tags: exiting. tag {} does not exist in netbox. Valid tags: {}'.format(tag, get_tags(self.nb)))
                    exit(1)
                tag_list.append(tag_id(self.nb, tag))
            return tag_list
        else:
            return None
