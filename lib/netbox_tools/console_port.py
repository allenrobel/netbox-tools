'''
Name: console_port.py
Description: Create, update, delete operations on netbox /dcim/console-ports/ endpoint
'''

from netbox_tools.common import device_id, get_tag, get_tags, tag_id

class ConsolePort(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_create_update_keys = ['device', 'port']
        self.mandatory_delete_keys = ['device', 'port']
        self.optional_keys = ['description', 'mark_connected', 'speed', 'type']
        self.port_speed_to_label = dict()
        self.port_speed_to_label[1200] = '1200 bps'
        self.port_speed_to_label[2400] = '2400 bps'
        self.port_speed_to_label[4800] = '4800 bps'
        self.port_speed_to_label[9600] = '9600 bps'
        self.port_speed_to_label[19200] = '19.2 kbps'
        self.port_speed_to_label[38400] = '38.4 kbps'
        self.port_speed_to_label[57600] = '57.6 kbps'
        self.port_speed_to_label[115200] = '115.2 kbps'

        self.port_type_to_label = dict()
        self.port_type_to_label['de-9'] = 'DE-9'
        self.port_type_to_label['db-25'] = 'DB-25'
        self.port_type_to_label['rj-11'] = 'RJ-11'
        self.port_type_to_label['rj-12'] = 'RJ-12'
        self.port_type_to_label['rj-45'] = 'RJ-45'
        self.port_type_to_label['mini-din-8'] = 'Mini-DIN 8'
        self.port_type_to_label['usb-a'] = 'USB Type A'
        self.port_type_to_label['usb-b'] = 'USB Type B'
        self.port_type_to_label['usb-c'] = 'USB Type C'
        self.port_type_to_label['usb-mini-a'] = 'USB Mini A'
        self.port_type_to_label['usb-mini-b'] = 'USB Mini B'
        self.port_type_to_label['usb-micro-a'] = 'USB Micro A'
        self.port_type_to_label['usb-micro-b'] = 'USB Micro B'
        self.port_type_to_label['usb-micro-ab'] = 'USB Micro AB'
        self.port_type_to_label['other'] = 'Other'

    def validate_delete_keys(self):
        for key in self.mandatory_delete_keys:
            if key not in self.info:
                print('ConsolePort.validate_delete_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def validate_create_update_keys(self):
        for key in self.mandatory_create_update_keys:
            if key not in self.info:
                print('ConsolePort.validate_create_update_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def populate_port_speed(self):
        if self.port_speed == None:
            return
        self.args['speed'] = dict()
        if self.port_speed not in self.port_speed_to_label:
            print('ConsolePort.populate_port_speed: exiting. Unknown port_speed.  Valid values are: {}'.format(','.join(self.port_speed_to_label.keys())))
            exit(1)
        # self.args['speed']['label'] = self.port_speed_to_label[self.port_speed]
        # self.args['speed']['value'] = self.port_speed
        self.args['speed'] = self.port_speed

    def populate_port_type(self):
        if self.port_type == None:
            return
        self.args['type'] = dict()
        if self.port_type not in self.port_type_to_label:
            print('ConsolePort.populate_port_type: exiting. Unknown port_type.  Valid values are: {}'.format(','.join(self.port_type_to_label.keys())))
            exit(1)
        # self.args['type']['label'] = self.port_type_to_label[self.port_type]
        # self.args['type']['value'] = self.port_type
        self.args['type'] = self.port_type

    def generate_create_update_args(self):
        self.args['name'] = self.port
        self.args['device'] = device_id(self.nb, self.device)
        if self.description != None:
            self.args['description'] = self.description
        if self.tags != None:
            self.args['tags'] = self.tags
        self.populate_port_speed()
        self.populate_port_type()

    def delete(self):
        self.validate_delete_keys()
        if self.console_port_object == None:
            print('ConsolePort.delete: Nothing to do. Device {} port {} does not exist in netbox.'.format(self.device, self.port))
            return
        print('ConsolePort.delete: device {} port {}'.format(self.device, self.port))
        try:
            self.console_port_object.delete()
        except Exception as e:
            print('ConsolePort.delete: Error. Unable to delete device {} port {}. Error was: {}'.format(self.device, self.port, e))
            return

    def create(self):
        print('ConsolePort.create: device {} port {}'.format(self.device, self.port))
        try:
            self.nb.dcim.console_ports.create(self.args)
        except Exception as e:
            print('ConsolePort.create: Exiting. Unable to create device {} port {}. Error was: {}'.format(self.device, self.port, e))
            exit(1)

    def update(self):
        print('ConsolePort.update: device {} port {}'.format(self.device, self.port))
        try:
            self.console_port_object.update(self.args)
        except Exception as e:
            print('ConsolePort.update: Exiting. Unable to update device {} port {}. Error was: {}'.format(self.device, self.port, e))
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
        try:
            return self.nb.dcim.console_ports.get(device=self.device, name=self.port)
        except Exception as e:
            print('ConsolePort: console_port_object: Exiting. dcim.console_ports.get() failed for device {} port {}.  Specific error was: {}'.format(
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
                    print('ConsolePort.tags: exiting. tag {} does not exist in netbox. Valid tags: {}'.format(tag, get_tags(self.nb)))
                    exit(1)
                tag_list.append(tag_id(self.nb, tag))
            return tag_list
        else:
            return None

    @property
    def port_speed(self):
        if 'port_speed' in self.info:
            return self.info['port_speed']
        else:
            return None

    @property
    def port_type(self):
        if 'port_type' in self.info:
            return self.info['port_type']
        else:
            return None
