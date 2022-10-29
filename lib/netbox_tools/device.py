'''
Name: device.py
Description: Class for create, update, and delete operations on netbox device
'''

from netbox_tools.common import create_slug
from netbox_tools.common import device_type_id, get_device
from netbox_tools.common import interface_id
from netbox_tools.common import ip_address_id, get_ip_address
from netbox_tools.common import location_id
from netbox_tools.common import rack_id
from netbox_tools.common import role_id
from netbox_tools.common import site_id
from netbox_tools.common import tag_id

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
        self.mandatory_keys_create_or_update = ['device', 'role', 'type']
        self.mandatory_keys_delete = ['device']
        self.fix_deprecations()

    def fix_deprecations(self):
        if 'mgmt_interface' in self.info:
            print('Device.fix_deprecations: WARNING: devices: <device>: mgmt_interface in your YAML file is deprecated. Use devices: <device>: interface instead.')
            self.info['interface'] = self.info['mgmt_interface']
        if 'name' in self.info:
            print('Device.fix_deprecations: WARNING: devices: <device>: name in your YAML file is deprecated. Use devices: <device>: device instead.')
            self.info['device'] = self.info['name']

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
        self.args['name'] = self.info['device']
        self.args['site'] = site_id(self.nb, self.site)
        self.args['slug'] = create_slug(self.info['device'])
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
        print('Device.create: {}'.format(self.device))
        try:
            self.nb.dcim.devices.create(self.args)
        except Exception as e:
            print('Device.create: Exiting. Unable to create device {}.  Error was: {}'.format(self.device, e))
            exit(1)

    def update(self):
        print('Device.update: {}'.format(self.device))
        self.args['id'] = self.device_id
        try:
            self.device_object.update(self.args)
        except Exception as e:
            print('Device.update: Exiting. Unable to update device {}.  Error was: {}'.format(self.device, e))
            exit(1)

    def delete(self):
        print('Device.delete: {}'.format(self.device))
        self.validate_keys_delete()
        if self.device_object == None:
            print('Device.delete: Nothing to do, device {} does not exist in netbox.'.format(self.device))
            return
        try:
            self.device_object.delete()
        except Exception as e:
            print('Device.delete: Exiting. Unable to delete device {}.  Error was: {}'.format(self.device, e))
            exit(1)

    def create_or_update(self):
        self.validate_keys_create_or_update()
        self.generate_args_create_or_update()
        if self.device_object == None:
            self.create()
        else:
            self.update()

    @property
    def device_object(self):
        return self.nb.dcim.devices.get(name=self.device)

    @property
    def device_id(self):
        return self.device_object.id

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

    # For backward-compatibility. Remove after 2023-09-29
    @property
    def name(self):
        return self.info['device']

    @property
    def device(self):
        return self.info['device']

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

