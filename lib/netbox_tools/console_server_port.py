'''
Name: console_server_port.py
Description: Create, update, delete operations on netbox /dcim/console-server-ports/ endpoint
'''

from netbox_tools.common import device_id, get_tag, get_tags, tag_id

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
        tags = self.tags
        if tags != None:
            self.args['tags'] = tags

    def delete(self):
        self.validate_delete_keys()
        if self.console_server_port_object == None:
            print('ConsoleServerPort.delete: Nothing to do. Device {} port {} does not exist in netbox.'.format(self.device, self.port))
            return
        print('ConsoleServerPort.delete: device {} port {}'.format(self.device, self.port))
        try:
            self.console_server_port_object.delete()
        except Exception as e:
            print('ConsoleServerPort.delete: Error. Unable to delete device {} port {}. Error was: {}'.format(self.device, self.port, e))
            return

    def create(self):
        print('ConsoleServerPort.create: device {} port {}'.format(self.device, self.port))
        try:
            self.nb.dcim.console_server_ports.create(self.args)
        except Exception as e:
            print('ConsoleServerPort.create: Exiting. Unable to create device {} port {}. Error was: {}'.format(self.device, self.port, e))
            exit(1)

    def update(self):
        print('ConsoleServerPort.update: device {} port {}'.format(self.device, self.port))
        try:
            self.console_server_port_object.update(self.args)
        except Exception as e:
            print('ConsoleServerPort.update: Exiting. Unable to update device {} port {}. Error was: {}'.format(self.device, self.port, e))
            exit(1)

    def create_or_update(self):
        self.validate_create_update_keys()
        self.generate_create_update_args()
        if self.console_server_port_object == None:
            self.create()
        else:
            self.update()

    @property
    def console_server_port_object(self):
        try:
            return self.nb.dcim.console_server_ports.get(device=self.device, name=self.port)
        except Exception as e:
            print('ConsoleServerPort: console_server_port_object: Exiting. dcim.console_server_ports.get() failed for device {} port {}.  Specific error was: {}'.format(
                self.device,
                self.port,
                e))
            exit(1)

    @property
    def description(self):
        if 'description' in self.info:
            return self.info['description']
        else:
            return None

    @property
    def device(self):
        return self.info['device']

    @property
    def port(self):
        return self.info['port']

    @property
    def tags(self):
        if 'tags' in self.info:
            tag_list = list()
            for tag in self.info['tags']:
                tag_obj = get_tag(self.nb, tag)
                if tag_obj == None:
                    print('DeviceType.tags: exiting. tag {} does not exist in netbox. Valid tags: {}'.format(tag, get_tags(self.nb)))
                    exit(1)
                tag_list.append(tag_id(self.nb, tag))
            return tag_list
        else:
            return None