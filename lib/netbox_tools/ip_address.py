'''
Name: ip_address.py
Description: Class for create and update operations on netbox ip_addresss
'''

from netbox_tools.common import device_id, get_device
from netbox_tools.common import interface_id

class IpAddress(object):
    '''
    nb = netbox instance
    info = dictionary with the following keys:
    {
        # mandatory
        device: device to which the interface belongs e.g. cvd_leaf_1
        interface: interface on which ip addresses will be assigned e.g. mgmt0, Eth1/1, Vlan150, etc
        ip4: ipv4 address for the interface e.g. 1.1.1.0/24
        # optional
        ip_description: free-form description of the ip address
        ip_status: status of the ip address. Valid values: active, reserved, deprecated, dhcp, slaac
    }
    '''
    def __init__(self, nb, info):
        self.version = 101
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['interface', 'ip4', 'device']
        self.optional_keys = ['ip_description', 'ip_status']
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
        self.args['address'] = self.ip4
        self.args['assigned_object_id'] = device_id(self.nb, self.device)
        self.args['interface'] = interface_id(self.nb, self.device, self.interface)
        if self.ip_description == None:
            self.args['description'] = '{} : {} : {}'.format(
                self.device,
                self.interface,
                self.ip4)
        else:
            self.args['description'] = self.ip_description
        if self.ip_status == None:
            self.args['status'] = 'active'
        else:
            self.args['status'] = self.ip_status

    def initialize_device_primary_ip(self):
        '''
        Initialize primary_ip4 and primary_ip to avoid errors in map_device_primary_ip()address.save()
        '''
        device = get_device(self.nb, self.device)
        device.primary_ip4 = None
        device.primary_ip = None
        device.save()

    def create(self):
        print('IpAddress.create: device {} address {}'.format(self.device, self.ip4))
        try:
            self.nb.ipam.ip_addresses.create(self.args)
        except Exception as e:
            print('IpAddress.create: Exiting. Unable to create device {} ip_address {}.  Error was: {}'.format(
                self.device,
                self.ip4,
                e))
            exit(1)

    def update(self):
        print('IpAddress.update: device {} address {}'.format(self.device, self.ip4))
        self.args['id'] = self.ip_address_id
        try:
            self.ip_address.update(self.args)
        except Exception as e:
            print('IpAddress.update: Exiting. Unable to update device {} ip_address {}.  Error was: {}'.format(
                self.device,
                self.ip4,
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
    def ip_description(self):
        if 'ip_description' in self.info:
            return self.info['ip_description']
        else:
            return None

    @property
    def ip_status(self):
        if 'ip_status' in self.info:
            return self.info['ip_status']
        else:
            return None

    @property
    def ip_address(self):
        try:
            address,mask = self.ip4.split('/')
        except Exception as e:
            print('IpAddress: exiting. Unexpected IP address format.  Expected A.B.C.D/E. Got {}. Specific error was: {}'.format(self.ip4, e))
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
    def ip4(self):
        return self.info['ip4']
