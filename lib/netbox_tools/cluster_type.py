'''
Name: cluster_type.py
Description: Class for create and update operations on netbox cluster_type
'''
import sys
from inspect import stack
from netbox_tools.common import create_slug, tag_id

OUR_VERSION = 102

class ClusterType():
    '''
    create, update, and delete operations on netbox virtualization.cluster_types
    '''
    def __init__(self, netbox, info):
        self._netbox = netbox
        self._info = info
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self.args = {}
        self._populate_mandatory_keys()
        self._populate_optional_keys()

    def _populate_mandatory_keys(self):
        '''
        The mandatory keys netbox expects to be present.  These are
        checked in self._validate_keys_create_update()
        '''
        self._mandatory_keys_create_update = set()
        self._mandatory_keys_create_update.add('name')

    def _populate_optional_keys(self):
        '''
        self._optional_keys are not used, currently.  They're just FYI.
        '''
        self._optional_keys = set()
        self._optional_keys.add('description')
        self._optional_keys.add('tags')


    def _log(self, msg):
        '''
        All logging output goes thru this.  We can change this to a proper logger later...
        '''
        print('{}(v{}).{}: {}'.format(self._classname, self.lib_version, stack()[1].function, msg))


    def _validate_keys_create_update(self):
        '''
        verify that all mandatory keys are present
        '''
        for key in self._mandatory_keys_create_update:
            if key not in self._info:
                self._log('exiting. mandatory key {} not found in info {}'.format(key, self._info))
                sys.exit(1)


    def _set_description(self):
        '''
        populate args with the cluster_type description
        '''
        if self.description is not None:
            self.args['description'] = self.description


    def _set_name(self):
        '''
        populate args with the cluster_type name
        '''
        self.args['name'] = self.name


    def _set_slug(self):
        '''
        populate args with a url-friendly name for the cluster_type
        If the caller has not set the slug, we do it here
        '''
        if self.slug is None:
            self.args['slug'] = create_slug(self.name)
        else:
            self.args['slug'] = self.slug


    def _set_tags(self):
        '''
        populate args with tags, if any
        '''
        if 'tags' not in self._info:
            return
        self.args['tags'] = []
        for tag in self._info['tags']:
            self.args['tags'].append(tag_id(self._netbox, tag))


    def _generate_args_create_update(self):
        '''
        generate all supported arguments
        '''
        self._set_description()
        self._set_name()
        self._set_slug()
        self._set_tags()


    def delete(self):
        '''
        delete a cluster_type
        '''
        self._log('{}'.format(self._info['name']))
        try:
            self.cluster_type_object.delete()
        except Exception as _general_error:
            self._log('WARNING. Unable to delete cluster_type {}.  Error was: {}'.format(self._info['name'], _general_error))
            return


    def create(self):
        '''
        create a cluster_type
        '''
        self._log('{}'.format(self._info['name']))
        try:
            self._netbox.virtualization.cluster_types.create(self.args)
        except Exception as _general_error:
            self._log('exiting. Unable to create cluster_type {}.  Error was: {}'.format(self._info['name'], _general_error))
            sys.exit(1)


    def update(self):
        '''
        update a cluster_type
        '''
        self._log('{}'.format(self._info['name']))
        try:
            self.cluster_type_object.update(self.args)
        except Exception as _general_error:
            self._log('exiting. Unable to update cluster_type {}.  Error was: {}'.format(self._info['name'], _general_error))
            sys.exit(1)


    def create_or_update(self):
        '''
        entry point into creation and updation methods
        '''
        self._validate_keys_create_update()
        self._generate_args_create_update()
        if self.cluster_type_object is None:
            self.create()
        else:
            self.update()


    @property
    def cluster_type_object(self):
        '''
        retrieve a cluster_type object from netbox by filtering on self.name and return it
        '''
        return self._netbox.virtualization.cluster_types.get(name=self.name)


    @property
    def cluster_type_id(self):
        '''
        return the netbox ID of a cluster_type object
        '''
        return self.cluster_type_object.id


    @property
    def description(self):
        '''
        set the description of the cluster_type
        '''
        if 'description' in self._info:
            return self._info['description']
        return None


    @property
    def name(self):
        '''
        set the name of the cluster_type. Used to check if the cluster_type
        already exists, and for the name of new cluster_types
        '''
        if 'name' in self._info:
            return self._info['name']
        return None

    @property
    def slug(self):
        '''
        set the slug (url friendly name) of the cluster_type.  If this
        is not set by the caller, we set it in self._set_slug()
        '''
        if 'slug' in self._info:
            return self._info['slug']
        return None

    @property
    def tags(self):
        '''
        set the cluster_type's tags
        '''
        if 'tags' in self._info:
            return self._info['tags']
        return None
