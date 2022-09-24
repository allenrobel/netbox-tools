'''
Name: ip_address.py
Description: Class for create and update operations on netbox ip_addresss
'''

from lib.common import device_id, get_device
from lib.common import interface_id

class IpAddress(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = ['mgmt_interface', 'mgmt_ip', 'name']
        self.optional_keys = ['interface_description', 'interface_status']
        self.default_ip_address_type = '1000base-t'
        self.default_ip_address_enabled = True
        self.validate_keys()
        self.generate_args()
        self.initialize_device_primary_ip()

    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('ip_address.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args(self):
        self.args['address'] = self.mgmt_ip
        self.args['assigned_object_id'] = device_id(self.nb, self.device)
        self.args['interface'] = interface_id(self.nb, self.device, self.mgmt_interface)
        if self.interface_description == None:
            self.args['description'] = '{} : {} : {}'.format(
                self.device,
                self.mgmt_interface,
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
        return self.info['name']

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
        address,mask = self.mgmt_ip.split('/')
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

    @property
    def mgmt_interface(self):
        return self.info['mgmt_interface']

    @property
    def mgmt_ip(self):
        return self.info['mgmt_ip']

# device_ip -----------------------------------------

# def initialize_device_primary_ip(name):
#     '''
#     name is typically found in device_info['name']
#     Initialize primary_ip4 and primary_ip to avoid errors in map_device_primary_ip()address.save()
#     '''
#     device = get_device(nb, name)
#     device.primary_ip4 = None
#     device.primary_ip = None
#     device.save()
#     print('initialize_device_primary_ip: device {} primary_ip and primary_ip4 DONE'.format(name))

# def get_ip_address(ip):
#     address,mask = ip.split('/')
#     try:
#         return nb.ipam.ip_addresses.get(address=address, mask=mask)
#     except:
#         return None

# def get_ip_address_id(ip):
#     address,mask = ip.split('/')
#     try:
#         ip_address = nb.ipam.ip_addresses.get(address=address, mask=mask)
#         return ip_address.id
#     except:
#         print('get_ip_address_id: Exiting. Could not get ID for ip address {}'.format(ip))
#         exit(1)

# def get_ip_address_args(info):
#     args = dict()
#     args['address'] = info['mgmt_ip']
#     if 'interface_status' in info:
#         args['status'] = info['interface_status']
#     else:
#         args['status'] = 'active'
#     if 'interface_description' in info:
#         args['description'] = info['interface_description']
#     else:
#         args['description'] = '{} : {} : {}'.format(
#             info['name'],
#             info['mgmt_interface'],
#             info['mgmt_ip'])
#     args['interface'] = interface_id(nb, info['name'], info['mgmt_interface'])
#     args['assigned_object_id'] = device_id(nb, info['name'])
#     return args

# def create_ip_address(info):
#     args = get_ip_address_args(info)
#     result = nb.ipam.ip_addresses.create(args)
#     print('create_ip_address: device {} address {} result {}'.format(
#         info['name'],
#         info['mgmt_ip'],
#         result))

# def update_ip_address(info, ip_address):
#     args = get_ip_address_args(info)
#     result = ip_address.update(args)
#     print('update_ip_address: device {} address {} result {}'.format(
#         info['name'],
#         info['mgmt_ip'],
#         result))

# def create_or_update_ip_address(info):
#     ip_address = get_ip_address(info['mgmt_ip'])
#     if ip_address  == None:
#         create_ip_address(info)
#     else:
#         update_ip_address(info, ip_address)

# def map_device_primary_ip(info):
#     '''
#     Map an existing IP address to an interface ID
#     '''
#     address = get_ip_address(info['mgmt_ip'])
#     address.assigned_object_id = interface_id(nb, info['name'], info['mgmt_interface'])
#     address.assigned_object_type = "dcim.interface"
#     address.save()
#     print('map_device_primary_ip: Map address {} to device {} interface {} DONE'.format(
#         info['name'],
#         info['mgmt_ip'],
#         info['mgmt_interface']))

# def make_device_primary_ip(info):
#     '''
#     Make an ip address the primary address for a device by mapping
#     the address ID to a device's primary_ip and primary_ip4.
#     '''
#     device = get_device(nb, info['name'])
#     ip_address_id = get_ip_address_id(info['mgmt_ip'])
#     device.primary_ip = ip_address_id
#     device.primary_ip4 = ip_address_id
#     device.save()
#     print('make_device_primary_ip: Make address {} (id {}) primary on device {} DONE'.format(
#         info['mgmt_ip'], ip_address_id, info['name']))

# def assign_primary_ip_to_device(info):
#     ipv4_id = get_ip_address_id(info['mgmt_ip'])
#     intf_id = interface_id(nb, info['name'], info['mgmt_interface'])
#     if ipv4_id == None:
#         print('assign_primary_ip_to_device: Exiting. Address {} not found in netbox'.format(info['mgmt_ip']))
#         exit(1)
#     if intf_id == None:
#         print('assign_primary_ip_to_device: Exiting. Interface {} not found in netbox'.format(info['mgmt_interface']))
#         exit(1)
#     initialize_device_primary_ip(info['name'])
#     map_device_primary_ip(info)
#     make_device_primary_ip(info)