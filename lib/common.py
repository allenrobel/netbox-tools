import re
from string import punctuation
import yaml

# device
def get_device(nb, name):
    '''
    Given netbox instance and device name, return device.
    If device does not exist in netbox, return None
    '''
    device = nb.dcim.devices.get(name=name)
    try:
        device = nb.dcim.devices.get(name=name)
        return device
    except Exception as e:
        print('common.get_device: returning None. exception was: {}'.format(e))
        return None

def device_id(nb, name):
    '''
    Given netbox instance and device name, return device_id.
    If device does not exist in netbox, return None
    '''
    try:
        device = nb.dcim.devices.get(name=name)
        return device.id
    except Exception as e:
        print('common.device_id: returning None. exception was: {}'.format(e))
        return None

# device_type
def get_device_type(nb, model):
    '''
    Given netbox instance and device_type model, return device_type.
    If device_type does not exist in netbox, return None
    '''
    try:
        device_type = nb.dcim.device_types.get(slug=model.lower())
        return device_type
    except Exception as e:
        print('common.get_device_type: returning None. exception was: {}'.format(e))
        return None

def device_type_id(nb, model):
    '''
    Given netbox instance and device_type model, return device_type_id.
    If device_type does not exist in netbox, return None
    '''
    try:
        device_type = nb.dcim.device_types.get(slug=model.lower())
        return device_type.id
    except Exception as e:
        print('common.device_type_id: returning None. exception was: {}'.format(e))
        return None

# interface
def get_interface(nb, device, name):
    '''
    Given netbox instance, device name, interface name, return interface object
    If interface does not exist in netbox, return None
    '''
    try:
        interface = nb.dcim.interfaces.get(
            name=name,
            device=device)
        return interface
    except Exception as e:
        print('common.get_interface: returning None. exception was: {}'.format(e))
        return None

def interface_id(nb, device, name):
    '''
    Given netbox instance, device name, interface name, return interface id
    If interface does not exist in netbox, return None
    '''
    try:
        interface = nb.dcim.interfaces.get(
            name=name,
            device=device)
        return interface.id
    except Exception as e:
        print('common.interface_id: returning None. exception was: {}'.format(e))
        return None


# ip address
def get_ip_address(nb, ip):
    '''
    Given netbox instance, and ip address with format A.B.C.D/E, return netbox ip address object.
    If address doesn't exist within netbox, return None
    '''
    address,mask = ip.split('/')
    try:
        return nb.ipam.ip_addresses.get(address=address, mask=mask)
    except Exception as e:
        print('common.get_ip_address: returning None. exception was: {}'.format(e))
        return None

def ip_address_id(nb, ip):
    '''
    Given netbox instance, and ip address with format A.B.C.D/E, return netbox ip address id.
    If ip address doesn't exist within netbox, return None
    '''
    address,mask = ip.split('/')
    try:
        ip_address = nb.ipam.ip_addresses.get(address=address, mask=mask)
        return ip_address.id
    except Exception as e:
        print('common.ip_address_id: returning None. exception was: {}'.format(e))
        return None

# location
def location_id(nb, name):
    '''
    Given netbox instance and location name, return location id.
    If location doesn't exist within netbox, return None
    '''
    try:
        location = nb.dcim.locations.get(name=name)
        return location.id
    except Exception as e:
        print('common.location_id: returning None. exception was: {}'.format(e))
        return None

# rack
def rack_id(nb, name):
    '''
    Given netbox instance and rack name, return rack id.
    If rack doesn't exist within netbox, return None
    '''
    try:
        rack = nb.dcim.racks.get(name=name)
        return rack.id
    except Exception as e:
        print('common.rack_id: returning None. exception was: {}'.format(e))
        return None

# manufacturer
def get_manufacturer(nb, name):
    '''
    Given netbox instance and manufacturer name, return manufacturer.
    If manufacturer doesn't exist within netbox, return None
    '''
    try:
        manufacturer = nb.dcim.manufacturers.get(name=name)
        return manufacturer
    except Exception as e:
        print('common.get_manufacturer: returning None. exception was: {}'.format(e))
        return None

def manufacturer_id(nb, name):
    '''
    Given netbox instance and manufacturer name, return manufacturer id.
    If manufacturer doesn't exist within netbox, return None
    '''
    try:
        manufacturer = nb.dcim.manufacturers.get(name=name)
        return manufacturer.id
    except Exception as e:
        print('common.manufacturer_id: returning None. exception was: {}'.format(e))
        return None

# role
def get_role(nb, name):
    '''
    Given netbox instance and device role name, return device role.
    If device role doesn't exist within netbox, return None
    '''
    try:
        role = nb.dcim.device_roles.get(name=name)
        return role
    except Exception as e:
        print('common.get_role: returning None. exception was: {}'.format(e))
        return None

def role_id(nb, name):
    '''
    Given netbox instance and role name, return role id.
    If device role doesn't exist within netbox, return None
    '''
    try:
        role = nb.dcim.device_roles.get(name=name)
        return role.id
    except Exception as e:
        print('common.role_id: returning None. exception was: {}'.format(e))
        return None

# site
def site_id(nb, name):
    '''
    Given netbox instance and site name, return site id.
    If site doesn't exist within netbox, return None
    '''
    try:
        site = nb.dcim.sites.get(name=name)
        return site.id
    except Exception as e:
        print('common.site_id: returning None. exception was: {}'.format(e))
        return None

# tag
def tag_id(nb, name):
    '''
    Given netbox instance and tag name, return tag id.
    If tag doesn't exist within netbox, return None
    '''
    try:
        tag = nb.extras.tags.get(name=name)
        return tag.id
    except Exception as e:
        print('common.tag_id: returning None. exception was: {}'.format(e))
        return None

# utility functions
def create_slug(s):
    '''
    Convert str() s into a slug that netbox accepts.
        1. remove all punctuation
        2. replace spaces with '-'
        3. convert to lower-case
    '''
    r = re.compile(r'[{}]+'.format(re.escape(punctuation)))
    s = r.sub('', s)
    s = s.replace(' ', '-')
    return s.lower()

def load_yaml(f):
    try:
        with open(f, 'r') as fh:
            contents = yaml.load(fh, Loader=yaml.FullLoader)
        return contents
    except Exception as e:
        print('common.load_yaml: exiting. Exception was: {}'.format(e))
