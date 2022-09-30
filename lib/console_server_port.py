'''
Name: console_server_port.py
Description: Create, update, delete operations on netbox /dcim/console-server-ports/ endpoint
'''

from lib.common import device_id

class ConsoleServerPort(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_create_update_keys = ['device', 'port']
        self.mandatory_delete_keys = ['device', 'port']
        self.optional_keys = ['description', 'mark_connected', 'speed']

    def validate_delete_keys(self):
        for key in self.mandatory_delete_keys:
            if key not in self.info:
                print('ConsoleServerPort.validate_delete_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def validate_create_update_keys(self):
        for key in self.mandatory_create_update_keys:
            if key not in self.info:
                print('ConsoleServerPort.validate_create_update_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def generate_create_update_args(self):
        self.args['name'] = self.port
        self.args['device'] = device_id(self.nb, self.device)
        if self.description != None:
            self.args['description'] = self.description

    def delete(self):
        self.validate_delete_keys()
        if self.manufacturer == None:
            print('ConsoleServerPort.delete: Nothing to do. Device {} port {} does not exist in netbox.'.format(self.device, self.port))
            return
        print('ConsoleServerPort.delete: {}'.format(self.name))
        try:
            self.manufacturer.delete()
        except Exception as e:
            print('ConsoleServerPort.delete: Error. Unable to delete device {} console_server_port {}.  Error was: {}'.format(self.device, self.port, e))
            return

    def create(self):
        print('ConsoleServerPort.create: device {} port {}'.format(self.device, self.port))
        try:
            self.nb.dcim.console_server_ports.create(self.args)
        except Exception as e:
            print('ConsoleServerPort.create: Exiting. Unable to create device {} port {}.  Error was: {}'.format(self.device, self.port, e))
            exit(1)

    def update(self):
        print('ConsoleServerPort.update: device {} port {}'.format(self.device, self.port))
        self.args['id'] = self.manufacturer_id
        try:
            self.console_port_object.update(self.args)
        except Exception as e:
            print('ConsoleServerPort.update: Exiting. Unable to update device {} port {}.  Error was: {}'.format(self.device, self.port, e))
            exit(1)

    def create_or_update(self):
        self.validate_create_update_keys()
        self.generate_create_update_args()
        if self.console_port_object == None:
            self.create()
        else:
            self.update()

    @property
    def console_port_object(self):
        return self.nb.dcim.console_server_ports.get(device=self.device, name=self.port)

    @property
    def device(self):
        return self.info['device']

    @property
    def port(self):
        return self.info['port']

    @property
    def description(self):
        if 'description' in self.info:
            return self.info['description']
        else:
            return None

