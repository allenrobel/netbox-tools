'''
Name: virtual_machine.py
Description: create/update/delete operations on netbox virtual_machine
'''
from inspect import stack, getframeinfo, currentframe
from netbox_tools.common import cluster_id
from netbox_tools.common import create_slug
from netbox_tools.common import device_id
from netbox_tools.common import get_vm
from netbox_tools.common import ip_address_id, get_ip_address
from netbox_tools.common import role_id
from netbox_tools.common import site_id
from netbox_tools.common import tag_id
from netbox_tools.common import virtual_interface_id

OUR_VERSION = 102

def initialize_vm_primary_ip(nb, vm_name):
    '''
    Initialize primary_ip4 and primary_ip to avoid errors in map_vm_primary_ip()address.save()
    '''
    vm = get_vm(nb, vm_name)
    vm.primary_ip4 = None
    vm.primary_ip = None
    vm.save()
    print('{}(v{}).{}: vm: {}'.format(__name__, OUR_VERSION, getframeinfo(currentframe()).function, vm_name))


def map_vm_primary_ip(nb, vm_name, interface_name, ip_address):
    '''
    Map an existing IP address to an interface ID

    args: nb, vm_name, interface_name, ip_address

    Where:

        nb - netbox instance

        vm_name - str() name of a virtual machine

        interface_name - str() name of an interface

        ip_address - str() ip address in A.B.C.D/E format    
    '''
    address = get_ip_address(nb, ip_address)
    address.assigned_object_id = virtual_interface_id(nb, vm_name, interface_name)
    address.assigned_object_type = "virtualization.vminterface"
    address.save()
    print('{}(v{}).{}: vm: {}, interface: {}, address: {}'.format(__name__, OUR_VERSION, getframeinfo(currentframe()).function, vm_name, interface_name, ip_address))

def make_vm_primary_ip(nb, vm, ip):
    '''
    Make an ip address the primary address for a virtual_machine by mapping
    the address ID to a virtual_machines's primary_ip and primary_ip4.
    '''
    vm = get_vm(nb, vm)
    address_id = ip_address_id(nb, ip)
    vm.primary_ip = address_id
    vm.primary_ip4 = address_id
    vm.save()
    print('{}(v{}).{}: vm: {}, ip: {}'.format(__name__, OUR_VERSION, getframeinfo(currentframe()).function, vm, ip))


class VirtualMachine(object):
    def __init__(self, netbox_obj, info):
        self.lib_version = OUR_VERSION
        self.classname = __class__.__name__
        self._netbox_obj = netbox_obj
        self._info = info
        self._args = dict()
        self.mandatory_keys_create_or_update = ['vm', 'role']
        self.mandatory_keys_delete = ['vm']

    def log(self, msg):
        print('{}(v{}).{}: {}'.format(self.classname, self.lib_version, stack()[1].function, msg))

    def validate_keys_delete(self):
        for key in self.mandatory_keys_delete:
            if key not in self._info:
                self.log('exiting. mandatory key {} not found in info {}'.format(key, self._info))
                exit(1)


    def validate_keys_create_or_update(self):
        for key in self.mandatory_keys_create_or_update:
            if key not in self._info:
                self.log('exiting. mandatory key {} not found in info {}'.format(key, self._info))
                exit(1)


    def set_cluster(self):
        if self.cluster != None:
            self._args['cluster'] = cluster_id(self._netbox_obj, self.cluster)


    def set_comments(self):
        if self.comments != None:
            self._args['comments'] = self.comments


    def set_device(self):
        '''device that hosts the virtual_machine'''
        if self.device != None:
            self._args['device'] = device_id(self._netbox_obj, self.device)


    def set_disk(self):
        if self.disk != None:
            self._args['disk'] = self.disk


    def set_memory(self):
        if self.memory != None:
            self._args['memory'] = self.memory


    def set_name(self):
        self._args['name'] = self.vm


    def set_role(self):
        if self.role != None:
            self._args['role'] = role_id(self._netbox_obj, self.role)


    def set_site(self):
        if self.site != None:
            self._args['site'] = site_id(self._netbox_obj, self.site)


    def set_slug(self):
        self._args['slug'] = create_slug(self._info['vm'])


    def _set_tags(self):
        """
        Add tags, if any, to args; converting them to netbox IDs
        """
        if self.tags is None:
            return
        self._args["tags"] = []
        for tag in self.tags:
            tid = tag_id(self._netbox_obj, tag)
            if tid is None:
                self.log(f"tag {tag} not found in Netbox.  Skipping.")
                continue
            self._args["tags"].append(tid)


    def set_vcpus(self):
        if self.vcpus != None:
            self._args['vcpus'] = self.vcpus


    def generate_args_create_or_update(self):
        self.set_comments()
        self.set_cluster()
        self.set_device()
        self.set_disk()
        self.set_memory()
        self.set_name()
        self.set_role()
        self.set_site()
        self.set_slug()
        self._set_tags()
        self.set_vcpus()


    def create(self):
        self.log('{}'.format(self.vm))
        try:
            self._netbox_obj.virtualization.virtual_machines.create(self._args)
        except Exception as e:
            self.log('exiting. Unable to create vm {}.  Error was: {}'.format(self.vm, e))
            exit(1)


    def update(self):
        self.log('{}'.format(self.vm))
        self._args['id'] = self.vm_id
        try:
            self.vm_object.update(self._args)
        except Exception as e:
            self.log('exiting. Unable to update vm {}.  Error was: {}'.format(self.vm, e))
            exit(1)


    def delete(self):
        self.log('{}'.format(self.device))
        self.validate_keys_delete()
        if self.vm_object == None:
            self.log('Nothing to do, vm {} does not exist in netbox.'.format(self.vm))
            return
        try:
            self.vm_object.delete()
        except Exception as e:
            self.log('exiting. Unable to delete vm {}.  Error was: {}'.format(self.vm, e))
            exit(1)


    def create_or_update(self):
        self.validate_keys_create_or_update()
        self.generate_args_create_or_update()
        if self.vm_object == None:
            self.create()
        else:
            self.update()


    @property
    def cluster(self):
        if 'cluster' in self._info:
            return self._info['cluster']
        else:
            return None


    @property
    def comments(self):
        if 'comments' in self._info:
            return self._info['comments']
        else:
            return None


    @property
    def device(self):
        '''
        The device hosting the virtual machine. device must already exist in netbox.
        If device is defined, cluster must also be defined.  We don't test for that
        here since netbox returns a good error message.
        '''
        if 'device' in self._info:
            return self._info['device']
        else:
            return None


    @property
    def disk(self):
        '''(int) disk space allocated to the vm, in GB'''
        if 'disk' in self._info:
            return self._info['disk']
        else:
            return None


    @property
    def memory(self):
        '''(int) memory allocated to the vm, in MB'''
        if 'memory' in self._info:
            return self._info['memory']
        else:
            return None


    @property
    def role(self):
        '''(str) role the vm serves. role must already exist in netbox'''
        if 'role' in self._info:
            return self._info['role']
        else:
            return None


    @property
    def site(self):
        '''site in which the vm is located. site must already exist in netbox'''
        if 'site' in self._info:
            return self._info['site']
        else:
            return None


    @property
    def tags(self):
        """
        Return the list of tag names set by the caller.
        If the caller didn't set this, return None.
        """
        if "tags" in self._info:
            return self._info["tags"]
        return None


    @property
    def vcpus(self):
        '''(float) virtual cpu units allocated to the vm. Min value: 0.01'''
        if 'vcpus' in self._info:
            try:
                vcpus = float(str(self._info['vcpus']))
            except:
                self.log('exiting. vcpus must be of type float. e.g. 1.01. Got {}'.format(self._info['vcpus']))
                exit(1)
            if vcpus < 0.01:
                self.log('exiting. vcpus must be greater than 0.01. Got {}'.format(self._info['vcpus']))
                exit(1)
            return self._info['vcpus']
        else:
            return None


    @property
    def vm(self):
        return self._info['vm']


    @property
    def vm_id(self):
        return self.vm_object.id


    @property
    def vm_object(self):
        return self._netbox_obj.virtualization.virtual_machines.get(name=self.vm)

