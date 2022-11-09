'''
Name: ip_prefix.py
Description: Class for create, update, delete operations on netbox ip_prefix
'''

from netbox_tools.common import device_id, get_device
from netbox_tools.common import site_id, vlan_vid_to_id

class IpPrefix(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['prefix']
        self.optional_keys = ['description', 'site', 'status', 'vlan', 'tags']
        self.default_status = 'active'
        self.validate_keys()
        self.generate_args()

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('ip_address.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['prefix'] = self.prefix
        if self.description != None:
            self.args['description'] = self.description
        if self.site != None:
            if self._site_id == None:
                print('IpPrefix.generate_args: exiting. prefix {} site {} does not exist in netbox. Either create the site first, or do not specify a site for this prefix.'.format(
                    self.prefix,
                    self.site))
                exit(1)
            self.args['site'] = self._site_id
        if self.status != None:
            self.args['status'] = self.status
        else:
            self.args['status'] = self.default_status
        if self.vlan != None:
            self.args['vlan'] = self.vlan_id

    def delete(self):
        print('IpPrefix.delete: prefix {}'.format(self.prefix))
        #self.args['id'] = self.prefix_id
        if self.prefix_object == None:
            print('IpPrefix.delete: Nothing to do. Prefix {} does not exist in netbox'.format(self.prefix))
            return
        try:
            self.prefix_object.delete()
        except Exception as e:
            print('IpPrefix.delete: Exiting. Unable to delete prefix {}.  Error was: {}'.format(
                self.prefix, e))
            exit(1)

    def create(self):
        print('IpPrefix.create: prefix {}'.format(self.prefix))
        try:
            self.nb.ipam.prefixes.create(self.args)
        except Exception as e:
            print('IpPrefix.create: Exiting. Unable to create prefix {}.  Error was: {}'.format(
                self.prefix,
                e))
            exit(1)

    def update(self):
        print('IpPrefix.update: prefix {}'.format(self.prefix))
        self.args['id'] = self.prefix_id
        try:
            self.prefix_object.update(self.args)
        except Exception as e:
            print('IpPrefix.update: Exiting. Unable to update prefix {}.  Error was: {}'.format(
                self.prefix, e))
            exit(1)

    def create_or_update(self):
        if self.prefix_object == None:
            self.create()
        else:
            self.update()

    @property
    def description(self):
        if 'description' in self.info:
            return self.info['description']
        else:
            return None

    @property
    def prefix_object(self):
        return self.nb.ipam.prefixes.get(prefix=self.prefix)

    @property
    def prefix(self):
        return self.info['prefix']

    @property
    def prefix_id(self):
        if self.prefix_object == None:
            print('IpPrefix.prefix_id: exiting. Unable to retrieve prefix {}'.format(self.prefix))
            exit(1)
        return self.prefix_object.id

    @property
    def site(self):
        if 'site' in self.info:
            return self.info['site']
        else:
            return None

    @property
    def _site_id(self):
        if 'site' in self.info:
            return site_id(self.nb, self.site)
        else:
            return None

    @property
    def status(self):
        if 'status' in self.info:
            return self.info['status']
        else:
            return None

    @property
    def vlan(self):
        '''Vlan vid'''
        if 'vlan' in self.info:
            return self.info['vlan']
        else:
            return None

    @property
    def vlan_id(self):
        '''Netbox ID of the vlan'''
        if 'vlan' in self.info:
            return vlan_vid_to_id(self.nb, self.vlan)
        else:
            return None
