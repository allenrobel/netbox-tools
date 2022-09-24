from lib.common import tag_id
from lib.common import create_slug

class Site(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['name']
        self.validate_keys()
        self.generate_args()

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

    def create(self):
        print('Site.create: {}'.format(self.name))
        try:
            self.nb.dcim.racks.create(self.args)
        except Exception as e:
            print('Site.create: Exiting. Unable to create site {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def update(self):
        print('Site.update: {}'.format(self.name))
        self.args['id'] = self.site_id
        try:
            self.site.update(self.args)
        except Exception as e:
            print('Site.update: Exiting. Unable to update site {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def create_or_update(self):
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
                tag_list.append(tag_id(self.nb, tag))
            return tag_list
        else:
            return None

# site -------------------------------------------
# def get_site_id(name):
#     site = nb.dcim.sites.get(name=name)
#     if site == None:
#         print('get_site_id: Exiting. Site {} not defined in netbox'.format(name))
#         exit(1)
#     return site.id

# def get_site_args(info):
#     mandatory_keys = ['name']
#     for key in mandatory_keys:
#         if key not in info:
#             print('get_site_args: exiting. mandatory key {} not found in info {}'.format(key, info))
#             exit(1)
#     args = dict()
#     args['name'] = info['name']
#     args['slug'] = create_slug(info['name'])
#     if 'description' in info:
#         args['description'] = info['description']
#     if 'tags' in info:
#         args['tags'] = list()
#         for tag in info['tags']:
#             args['tags'].append(get_tag_id(tag))
#     return args

# def update_site(info, site):
#     args = get_site_args(info)
#     args['id'] = site.id
#     nb.dcim.sites.update([args])
#     print('update_site: {}'.format(info['name']))

# def create_site(info):
#     args = get_site_args(info)
#     nb.dcim.sites.create(args)
#     print('create_site: {}'.format(info['name']))

# def create_or_update_site(info):
#     site = nb.dcim.sites.get(name=info['name'])
#     if site == None:
#         create_site(info)
#     else:
#         update_site(info, site)
