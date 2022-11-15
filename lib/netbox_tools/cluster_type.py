'''
Name: cluster_type.py
Description: Class for create and update operations on netbox cluster_type
'''

from netbox_tools.common import create_slug, tag_id

class ClusterType(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys_create_update = set()
        self.mandatory_keys_create_update.add('name')

        self.optional_keys = set()
        self.optional_keys.add('description')
        self.optional_keys.add('tags')

    def validate_keys_create_update(self):
        for key in self.mandatory_keys_create_update:
            if key not in self.info:
                print('ClusterType.validate_keys_create_update: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def set_description(self):
        if self.description != None:
            self.args['description'] = self.description

    def set_name(self):
        self.args['name'] = self.name

    def set_slug(self):
        self.args['slug'] = create_slug(self.name)

    def set_tags(self):
        if 'tags' in self.info:
            self.args['tags'] = list()
            for tag in self.info['tags']:
                self.args['tags'].append(tag_id(self.nb, tag))

    def generate_args_create_update(self):
        self.set_description()
        self.set_name()
        self.set_slug()
        self.set_tags()

    def delete(self):
        print('ClusterType.delete: {}'.format(self.info['name']))
        try:
            self.cluster_object.delete()
        except Exception as e:
            print('ClusterType.delete: WARNING. Unable to delete cluster_type {}.  Error was: {}'.format(self.info['name'], e))
            return

    def create(self):
        print('ClusterType.create: {}'.format(self.info['name']))
        try:
            self.nb.virtualization.cluster_types.create(self.args)
        except Exception as e:
            print('ClusterType.create: Exiting. Unable to create cluster_type {}.  Error was: {}'.format(self.info['name'], e))
            exit(1)

    def update(self):
        print('ClusterType.update: {}'.format(self.info['name']))
        self.args['id'] = self.cluster_id
        try:
            self.cluster_type_object.update(self.args)
        except Exception as e:
            print('ClusterType.update: Exiting. Unable to update cluster_type {}.  Error was: {}'.format(self.info['name'], e))
            exit(1)

    def create_or_update(self):
        self.validate_keys_create_update()
        self.generate_args_create_update()
        if self.cluster_type_object == None:
            self.create()
        else:
            self.update()

    @property
    def cluster_type_object(self):
        return self.nb.virtualization.cluster_types.get(name=self.name)

    @property
    def cluster_type_id(self):
        return self.cluster_type_object.id

    @property
    def description(self):
        if 'description' in self.info:
            return self.info['description']
        else:
            return None

    @property
    def name(self):
        if 'name' in self.info:
            return self.info['name']
        else:
            return None

    @property
    def tags(self):
        if 'tags' in self.info:
            return self.info['tags']
        else:
            return None