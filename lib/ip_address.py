'''
Name: ip_address.py
Description: Class for create and update operations on netbox ip_addresss
'''

from lib.common import device_id, get_device
from lib.common import interface_id

class IpAddress(object):
    def __init__(self, nb, info):
        self.version = 101
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['interface', 'mgmt_ip', 'device']
        self.optional_keys = ['interface_description', 'interface_status']
        self.default_ip_address_type = '1000base-t'
        self.default_ip_address_enabled = True
        self.fix_deprecations()
        self.validate_keys()
        self.generate_args()
        self.initialize_device_primary_ip()

    def fix_deprecations(self):
        if 'mgmt_interface' in self.info:
            print('IpAddress.fix_deprecations: WARNING: devices: <device>: mgmt_interface in your YAML file is deprecated. Use devices: <device>: interface instead.')
            self.info['interface'] = self.info['mgmt_interface']
        if 'name' in self.info:
            print('IpAddress.fix_deprecations: WARNING: devices: <device>: name in your YAML file is deprecated. Use devices: <device>: device instead.')
            self.info['device'] = self.info['name']

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('IpAddress.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['address'] = self.mgmt_ip
        self.args['assigned_object_id'] = device_id(self.nb, self.device)
        self.args['interface'] = interface_id(self.nb, self.device, self.interface)
        if self.interface_description == None:
            self.args['description'] = '{} : {} : {}'.format(
                self.device,
                self.interface,
                self.mgmt_ip)
        else:
            self.args['description'] = self.interface_description
        if self.interface_status == None:
            self.args['status'] = 'active'
        else:
            self.args['status'] = self.interface_status

    def initialize_device_primary_ip(self):
        '''
        Initialize primary_ip4 and primary_ip to avoid errors in map_device_primary_ip()address.save()
        '''
        device = get_device(self.nb, self.device)
        device.primary_ip4 = None
        device.primary_ip = None
        device.save()
        print('IpAddress.initialize_device_primary_ip: device {} primary_ip and primary_ip4'.format(self.device))

    def create(self):
        print('IpAddress.create: device {} address {}'.format(self.device, self.mgmt_ip))
        try:
            self.nb.ipam.ip_addresses.create(self.args)
        except Exception as e:
            print('IpAddress.create: Exiting. Unable to create device {} ip_address {}.  Error was: {}'.format(
                self.device,
                self.mgmt_ip,
                e))
            exit(1)

    def update(self):
        print('IpAddress.update: device {} address {}'.format(self.device, self.mgmt_ip))
        self.args['id'] = self.ip_address_id
        try:
            self.ip_address.update(self.args)
        except Exception as e:
            print('IpAddress.update: Exiting. Unable to update device {} ip_address {}.  Error was: {}'.format(
                self.device,
                self.mgmt_ip,
                e))
            exit(1)

    def create_or_update(self):
        if self.ip_address == None:
            self.create()
        else:
            self.update()

    @property
    def device(self):
        return self.info['device']

    @property
    def interface_description(self):
        if 'interface_description' in self.info:
            return self.info['interface_description']
        else:
            return None

    @property
    def interface_status(self):
        if 'interface_status' in self.info:
            return self.info['interface_status']
        else:
            return None

    @property
    def ip_address(self):
        try:
            address,mask = self.mgmt_ip.split('/')
        except Exception as e:
            print('IpAddress: exiting. Unexpected IP address format.  Expected A.B.C.D/E. Got {}. Specific error was: {}'.format(self.mgmt_ip, e))
            exit(1)
        return self.nb.ipam.ip_addresses.get(
            address=address,
            mask=mask)

    @property
    def ip_address_enabled(self):
        if 'ip_address_enabled' in self.info:
            return self.info['ip_address_enabled']
        else:
            return None

    @property
    def ip_address_id(self):
        return self.ip_address.id

    @property
    def ip_address_type(self):
        if 'ip_address_type' in self.info:
            return self.info['ip_address_type']
        else:
            return None

    # Keeping for backward-compatibility. Remove after 2023-09-29.
    @property
    def mgmt_interface(self):
        return self.info['interface']

    @property
    def interface(self):
        return self.info['interface']

    @property
    def mgmt_ip(self):
        return self.info['mgmt_ip']
