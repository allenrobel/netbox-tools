'''
Name: virtual_ip_address.py
Description: Class for create and update operations on netbox ip_addresss for virtual machines
'''

from netbox_tools.common import get_vm, vm_id

class VirtualIpAddress(object):
    '''
    nb = netbox instance
    info = dictionary with the following keys:
    {
        # mandatory
        virtual_machine: vm to which the interface belongs e.g. netbox_vm
        interface: interface on which ip addresses will be assigned e.g. vmnet0, etc
        ip4: ipv4 address for the interface e.g. 1.1.1.0/24
        # optional
        ip_description: free-form description of the ip address
        ip_status: status of the ip address. Valid values: active, reserved, deprecated, dhcp, slaac
    }
    '''
    def __init__(self, nb, info):
        self.version = 100
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys = set()
        self.mandatory_keys.add('interface')
        self.mandatory_keys.add('ip4')
        self.mandatory_keys.add('virtual_machine')
        self.optional_keys = set()
        self.optional_keys.add('ip_description')
        self.optional_keys.add('ip_status')
        self.validate_keys()
        self.generate_args()
        self.initialize_vm_primary_ip()


    def validate_keys(self):
        for key in self.mandatory_keys:
            if key not in self.info:
                print('VirtualIpAddress.validate_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)


    def set_address(self):
        self.args['address'] = self.ip4


    def set_assigned_object_id(self):
        self.args['assigned_object_id'] = vm_id(self.nb, self.virtual_machine)


    def set_description(self):
        if self.ip_description == None:
            self.args['description'] = '{} : {}'.format(
                self.virtual_machine,
                self.ip4)
        else:
            self.args['description'] = self.ip_description


    def set_interface(self):
        self.args['interface'] = vm_id(self.nb, self.virtual_machine)


    def set_status(self):
        if self.ip_status == None:
            self.args['status'] = 'active'
        else:
            self.args['status'] = self.ip_status


    def generate_args(self):
        self.set_address()
        self.set_assigned_object_id()
        self.set_description()
        self.set_interface()
        self.set_status()


    def initialize_vm_primary_ip(self):
        '''
        Initialize primary_ip4 and primary_ip to avoid errors in map_vm_primary_ip()address.save()
        '''
        vm = get_vm(self.nb, self.virtual_machine)
        vm.primary_ip4 = None
        vm.primary_ip = None
        vm.save()


    def create(self):
        print('VirtualIpAddress.create: virtual_machine {} address {}'.format(self.virtual_machine, self.ip4))
        try:
            self.nb.ipam.ip_addresses.create(self.args)
        except Exception as e:
            print('VirtualIpAddress.create: Exiting. Unable to create virtual_machine {} ip_address {}.  Error was: {}'.format(
                self.virtual_machine,
                self.ip4,
                e))
            exit(1)


    def update(self):
        print('VirtualIpAddress.update: virtual_machine {} address {}'.format(self.virtual_machine, self.ip4))
        self.args['id'] = self.ip_address_id
        try:
            self.ip_address.update(self.args)
        except Exception as e:
            print('VirtualIpAddress.update: Exiting. Unable to update virtual_machine {} ip_address {}.  Error was: {}'.format(
                self.virtual_machine,
                self.ip4,
                e))
            exit(1)


    def delete(self):
        print('VirtualIpAddress.delete: virtual_machine {} address {}'.format(self.virtual_machine, self.ip4))
        try:
            self.ip_address.delete()
        except Exception as e:
            print('VirtualIpAddress.delete: Exiting. Unable to delete virtual_machine {} ip_address {}.  Error was: {}'.format(
                self.virtual_machine,
                self.ip4,
                e))
            exit(1)


    def create_or_update(self):
        if self.ip_address == None:
            self.create()
        else:
            self.update()


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
            print('VirtualIpAddress: exiting. Unexpected IP address format.  Expected A.B.C.D/E. Got {}. Specific error was: {}'.format(self.ip4, e))
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


    @property
    def interface(self):
        return self.info['interface']


    @property
    def ip4(self):
        return self.info['ip4']


    @property
    def virtual_machine(self):
        return self.info['virtual_machine']
