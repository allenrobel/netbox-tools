'''
Name: cluster.py
Description: Class for create and update operations on netbox cluster
'''
our_version = 101
from inspect import stack, getframeinfo, currentframe
from netbox_tools.common import create_slug
from netbox_tools.common import cluster_group_id, cluster_type_id, site_id, tag_id

class Cluster(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.lib_version = our_version
        self.classname = __class__.__name__
        self.args = dict()
        self.mandatory_keys_create_update = set()
        self.mandatory_keys_create_update.add('cluster')
        self.mandatory_keys_create_update.add('type')

        self.mutex_keys = set()
        self.mutex_keys.add('site')
        self.mutex_keys.add('group')


    def log(self, msg):
        print('{}(v{}).{}: {}'.format(self.classname, self.lib_version, stack()[1].function, msg))


    def validate_keys_create_update(self):
        for key in self.mandatory_keys_create_update:
            if key not in self.info:
                self.log('exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)


    def test_mutex(self, test_key):
        if test_key not in self.info:
            return
        if self.info[test_key] == None:
            return
        for key in self.mutex_keys:
            if key == test_key:
                continue
            if key not in self.info:
                continue
            if self.info[key] != None:
                self.log('exiting. {test_key} is set and is mutually-exclusive to {key}.  Unset {test_key} or {key} and try again.'.format(
                    test_key=test_key,
                    key=key))
                exit(1)


    def set_group(self):
        self.test_mutex('group')
        if self.group != None:
            self.args['group'] = cluster_group_id(self.nb, self.info['group'])


    def set_name(self):
        self.args['name'] = self.info['cluster']


    def set_site(self):
        self.test_mutex('site')
        if self.site != None:
            self.args['site'] = site_id(self.nb, self.site)


    def set_tags(self):
        if 'tags' not in self.info:
            return
        self.args['tags'] = list()
        for tag in self.info['tags']:
            self.args['tags'].append(tag_id(self.nb, tag))


    def set_type(self):
        self.args['type'] = cluster_type_id(self.nb, self.type)


    def generate_args_create_update(self):
        self.set_group()
        self.set_name()
        self.set_site()
        self.set_tags()
        self.set_type()
        # self.args['slug'] = create_slug(self.info['name'])


    def delete(self):
        self.log('{}'.format(self.info['name']))
        try:
            self.cluster_object.delete()
        except Exception as e:
            self.log('WARNING. Unable to delete cluster {}.  Error was: {}'.format(self.info['name'], e))
            return


    def create(self):
        self.log('{}'.format(self.info['cluster']))
        try:
            self.nb.virtualization.clusters.create(self.args)
        except Exception as e:
            self.log('exiting. Unable to create cluster {}.  Error was: {}'.format(self.info['cluster'], e))
            exit(1)


    def update(self):
        self.log('{}'.format(self.info['cluster']))
        self.args['id'] = self.cluster_id
        try:
            self.cluster_object.update(self.args)
        except Exception as e:
            self.log('exiting. Unable to update cluster {}.  Error was: {}'.format(self.info['cluster'], e))
            exit(1)


    def create_or_update(self):
        self.validate_keys_create_update()
        self.generate_args_create_update()
        if self.cluster_object == None:
            self.create()
        else:
            self.update()


    @property
    def cluster(self):
        if 'cluster' in self.info:
            return self.info['cluster']
        else:
            return None


    @property
    def cluster_object(self):
        return self.nb.virtualization.clusters.get(name=self.cluster)


    @property
    def cluster_id(self):
        return self.cluster_object.id


    @property
    def group(self):
        if 'group' in self.info:
            return self.info['group']
        else:
            return None


    @property
    def site(self):
        if 'site' in self.info:
            return self.info['site']
        else:
            return None


    @property
    def type(self):
        if 'type' in self.info:
            return self.info['type']
        else:
            return None
