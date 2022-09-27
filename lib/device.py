'''
Name: device.py
Description: Class for create, update, and delete operations on netbox device
'''

from lib.common import create_slug
from lib.common import device_type_id, get_device
from lib.common import interface_id
from lib.common import ip_address_id, get_ip_address
from lib.common import location_id
from lib.common import rack_id
from lib.common import role_id
from lib.common import site_id
from lib.common import tag_id

def initialize_device_primary_ip(nb, device_name):
    '''
    Initialize primary_ip4 and primary_ip to avoid errors in map_device_primary_ip()address.save()
    '''
    device = get_device(nb, device_name)
    device.primary_ip4 = None
    device.primary_ip = None
    device.save()
    print('device.initialize_device_primary_ip: device {} primary_ip and primary_ip4'.format(device_name))

def map_device_primary_ip(nb, device_name, interface_name, ip_address):
    '''
    Map an existing IP address to an interface ID

    args: nb, device_name, interface_name, ip_address

    Where:

        nb - netbox instance

        device_name - str() name of a device

        interface_name - str() name of an interface

        ip_address - str() ip address in A.B.C.D/E format    
    '''
    address = get_ip_address(nb, ip_address)
    address.assigned_object_id = interface_id(nb, device_name, interface_name)
    address.assigned_object_type = "dcim.interface"
    address.save()
    print('device.map_device_primary_ip: device {} interface {} address {}'.format(
        device_name,
        interface_name,
        ip_address))

def make_device_primary_ip(nb, device_name, ip):
    '''
    Make an ip address the primary address for a device by mapping
    the address ID to a device's primary_ip and primary_ip4.
    '''
    device = get_device(nb, device_name)
    address_id = ip_address_id(nb, ip)
    device.primary_ip = address_id
    device.primary_ip4 = address_id
    device.save()
    print('device.make_device_primary_ip: device {} ip {}'.format(device_name, ip))

class Device(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys_create_or_update = ['name', 'role', 'type']
        self.mandatory_keys_delete = ['name']

    def validate_keys_delete(self):
        for key in self.mandatory_keys_delete:
            if key not in self.info:
                print('Device.validate_keys_delete: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def validate_keys_create_or_update(self):
        for key in self.mandatory_keys_create_or_update:
            if key not in self.info:
                print('Device.validate_keys_create_or_update: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_args_create_or_update(self):
        self.args['device_role'] = role_id(self.nb, self.device_role)
        self.args['device_type'] = device_type_id(self.nb, self.device_type)
        self.args['name'] = self.info['name']
        self.args['site'] = site_id(self.nb, self.site)
        self.args['slug'] = create_slug(self.info['name'])
        if self.face != None:
            self.args['face'] = self.face
        if self.location != None:
            self.args['location'] = location_id(self.nb, self.location)
        if self.position != None:
            self.args['position'] = self.position
        if self.rack != None:
            self.args['rack'] = rack_id(self.nb, self.rack)
        if self.serial != None:
            self.args['serial'] = self.serial
        if self.tags !=None:
            self.args['tags'] = self.tags

    def create(self):
        print('Device.create: {}'.format(self.name))
        try:
            self.nb.dcim.devices.create(self.args)
        except Exception as e:
            print('Device.create: Exiting. Unable to create device {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def update(self):
        print('Device.update: {}'.format(self.name))
        self.args['id'] = self.device_id
        try:
            self.device.update(self.args)
        except Exception as e:
            print('Device.update: Exiting. Unable to update device {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def delete(self):
        print('Device.delete: {}'.format(self.name))
        self.validate_keys_delete()
        if self.device == None:
            print('Device.delete: Nothing to do, device {} does not exist in netbox.'.format(self.name))
            return
        try:
            self.device.delete()
        except Exception as e:
            print('Device.delete: Exiting. Unable to delete device {}.  Error was: {}'.format(self.name, e))
            exit(1)

    def create_or_update(self):
        self.validate_keys_create_or_update()
        self.generate_args_create_or_update()
        if self.device == None:
            self.create()
        else:
            self.update()

    @property
    def device(self):
        return self.nb.dcim.devices.get(name=self.name)

    @property
    def device_id(self):
        return self.device.id

    @property
    def device_role(self):
        return self.info['role']

    @property
    def device_type(self):
        return self.info['type']

    @property
    def face(self):
        if 'face' in self.info:
            return self.info['face']
        else:
            return None

    @property
    def location(self):
        if 'location' in self.info:
            return self.info['location']
        else:
            return None

    @property
    def name(self):
        return self.info['name']

    @property
    def position(self):
        if 'position' in self.info:
            return self.info['position']
        else:
            return None

    @property
    def rack(self):
        if 'rack' in self.info:
            return self.info['rack']
        else:
            return None

    @property
    def serial(self):
        if 'serial' in self.info:
            return self.info['serial']
        else:
            return None

    @property
    def site(self):
        return self.info['site']

    @property
    def tags(self):
        if 'tags' in self.info:
            tag_list = list()
            for tag in self.info['tags']:
                tag_list.append(tag_id(self.nb, tag))
            return tag_list
        else:
            return None

