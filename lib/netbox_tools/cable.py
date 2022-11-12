'''
Name: cable.py
Description: Class for create, update, and delete operations on netbox cable
'''

# from netbox_tools.common import cable_id
# from netbox_tools.common import create_slug
# from netbox_tools.common import device_id
from netbox_tools.common import interface_id
from netbox_tools.common import tag_id
from netbox_tools.colors import color_to_rgb

class Cable(object):
    def __init__(self, nb, info):
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_keys_create_or_update = set()
        self.mandatory_keys_create_or_update.add('label') # A UNIQUE label to identify the cable
        self.mandatory_keys_create_or_update.add('device_a') # termination_a device name
        self.mandatory_keys_create_or_update.add('device_b') # termination_b device name
        self.mandatory_keys_create_or_update.add('port_a') # termination_a port name
        self.mandatory_keys_create_or_update.add('port_b') # termination_b port name
        self.mandatory_keys_create_or_update.add('port_a_type') # termination_a port type: interface, console, console_server, power
        self.mandatory_keys_create_or_update.add('port_b_type') # termination_a port type: interface, console, console_server, power
        self.mandatory_keys_delete = set()
        self.mandatory_keys_delete.add('label')
        self.optional_keys = set()
        self.optional_keys.add('color') # str - a color from colors.py in this repo, or a hex rgb color value, e.g. for red: f44336
        self.optional_keys.add('length') # int
        self.optional_keys.add('length_unit') # str
        self.optional_keys.add('status') # str
        self.optional_keys.add('tags') # a list of tags to associate with the cable
        self.optional_keys.add('type') # str
        self.valid_port_types = set()
        self.valid_port_types.add('interface')
        self.valid_port_types.add('console_server')
        self.valid_port_types.add('console')
        self.valid_port_types.add('power')
        self.port_type_map = dict()
        self.port_type_map['interface'] = 'dcim.interface'
        self.port_type_map['console_server'] = 'dcim.console_server_port'
        self.port_type_map['console'] = 'dcim.console_port'
        self.port_type_map['power'] = 'dcim.power_outlet'
        self.populate_valid_choices()

    def populate_valid_choices(self):
        self.valid_choices = dict()
        choices_dict = self.nb.dcim.cables.choices()
        for item in choices_dict:
            valid_values = choices_dict[item]
            self.valid_choices[item] = [item['value'] for item in valid_values]

    def validate_keys_delete(self):
        for key in self.mandatory_keys_delete:
            if key not in self.info:
                print('Cable.validate_keys_delete: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def validate_keys_create_or_update(self):
        for key in self.mandatory_keys_create_or_update:
            if key not in self.info:
                print('Cable.validate_keys_create_or_update: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def set_cable_type(self):
        if self.cable_type == None:
            return
        if self.cable_type in self.valid_choices['type']:
            self.args['type'] = self.cable_type
        else:
            print('Cable.set_cable_type: exiting. Invalid cable_type. Got {}. Expected one of {}.'.format(
                self.cable_type,
                ','.join(sorted(self.valid_choices['type']))))
            exit(1)

    def set_color(self):
        if self.rgb == None:
            return
        self.args['color'] = self.rgb

    def set_label(self):
        self.args['label'] = self.label

    def set_length(self):
        if self.length == None:
            return
        if isinstance(self.length, int):
            self.args['length'] = self.length
        else:
            print('Cable.set_length: exiting. Expected type int for length. Got {}'.format(self.length))
            exit(1)

    def set_length_unit(self):
        if self.length_unit == None:
            return
        if self.length_unit in self.valid_choices['length_unit']:
            self.args['length_unit'] = self.length_unit
        else:
            print('Cable.set_length_unit: exiting. Invalid length_unit. Got {}. Expected one of {}.'.format(
                self.length_unit,
                ','.join(sorted(self.valid_choices['length_unit']))))
            exit(1)

    def set_status(self):
        if self.status == None:
            return
        if self.status in self.valid_choices['status']:
            self.args['status'] = self.status
        else:
            print('Cable.set_status: exiting. Invalid status. Got {}. Expected one of {}.'.format(
                self.status,
                ','.join(sorted(self.valid_choices['status']))))
            exit(1)

    def set_a_terminations(self):
        if self.device_a == None:
            print('Cable.set_a_terminations: exiting. Missing mandatory parameter: device_a')
            exit(1)
        if self.port_a == None:
            print('Cable.set_a_terminations: exiting. Missing mandatory parameter: port_a')
            exit(1)
        if self.port_a_type == None:
            print('Cable.set_a_terminations: exiting. Missing mandatory parameter: port_a_type')
            exit(1)
        if self.port_a_type not in self.valid_port_types:
            print('Cable.set_a_terminations: exiting. Unexpected port_a_type. Got {}. Expected one of {}.'.format(
                self.port_a_type,
                ','.join(self.valid_port_types)))
            exit(1)
        self.args['a_terminations'] = list()
        termination = dict()
        termination['object_id'] = interface_id(self.nb, self.device_a, self.port_a)
        termination['object_type'] = self.port_type_map[self.port_a_type]
        self.args['a_terminations'].append(termination)

    def set_b_terminations(self):
        if self.device_b == None:
            print('Cable.set_b_terminations: exiting. Missing mandatory parameter: device_b')
            exit(1)
        if self.port_b == None:
            print('Cable.set_b_terminations: exiting. Missing mandatory parameter: port_b')
            exit(1)
        if self.port_b_type == None:
            print('Cable.set_b_terminations: exiting. Missing mandatory parameter: port_b_type')
            exit(1)
        if self.port_b_type not in self.valid_port_types:
            print('Cable.set_b_terminations: exiting. Unexpected port_b_type. Got {}. Expected one of {}.'.format(
                self.port_b_type,
                ','.join(self.valid_port_types)))
            exit(1)
        self.args['b_terminations'] = list()
        termination = dict()
        termination['object_id'] = interface_id(self.nb, self.device_b, self.port_b)
        termination['object_type'] = self.port_type_map[self.port_b_type]
        self.args['b_terminations'].append(termination)

    def set_tags(self):
        if self.tags != None:
            self.args['tags'] = self.tags

    def generate_args_create_or_update(self):
        self.set_cable_type()
        self.set_color()
        self.set_label()
        self.set_length_unit()
        self.set_status()
        self.set_length()
        self.set_a_terminations()
        self.set_b_terminations()
        self.set_tags()

    def create(self):
        print('Cable.create: {}'.format(self.label))
        try:
            self.nb.dcim.cables.create(self.args)
        except Exception as e:
            print('Cable.create: Exiting. Unable to create Cable {}.  Error was: {}'.format(self.label, e))
            exit(1)

    def update(self):
        # There's a bug that causes update not to work for cable.
        # https://github.com/netbox-community/pynetbox/issues/491
        # For now, we delete the cable, then recreate it with the new args.
        # This results in the cable_id changing though, which isn't ideal since change log will only
        # ever have one entry, and journel entries will be deleted.
        print('Cable.update: {} cable_id {}'.format(self.label, self.cable_id))
        try:
            self.cable_object.delete()
        except Exception as e:
            print('Cable.update: Unable to delete cable {} prior to recreate due to {}'.format(self.label, e))
            print('Cable.update: proceeding nonetheless...')
            pass
        try:
            self.nb.dcim.cables.create(self.args)
        except Exception as e:
            print('Cable.update: Exiting. Unable to create Cable {}.  Error was: {}'.format(self.label, e))
            exit(1)

    # def update(self):
    #     print('Cable.update: {} cable_id {}'.format(self.label, self.cable_id))
    #     try:
    #         self.cable_object.update(self.args)
    #     except Exception as e:
    #         print('Cable.update: Unable to update cable {}. Error was: {}'.format(self.label, e))
    #         print('Cable.update: args: {}'.format(self.args))
    #         exit(1)

    def delete(self):
        print('Cable.delete: {}'.format(self.label))
        self.validate_keys_delete()
        if self.cable_object == None:
            print('Cable.delete: Nothing to do, Cable {} does not exist in netbox.'.format(self.label))
            return
        try:
            self.cable_object.delete()
        except Exception as e:
            print('Cable.delete: Exiting. Unable to delete Cable {}.  Error was: {}'.format(self.label, e))
            exit(1)

    def create_or_update(self):
        self.validate_keys_create_or_update()
        self.generate_args_create_or_update()
        if self.cable_object == None:
            self.create()
        else:
            self.update()

    @property
    def color(self):
        if 'color' in self.info:
            return self.info['color']
        else:
            return None

    @property
    def rgb(self):
        if self.color == None:
            return None
        return color_to_rgb(self.info['color'])

    @property
    def label(self):
        return self.info['label']

    @property
    def cable_object(self):
        return self.nb.dcim.cables.get(label=self.label)

    @property
    def cable_id(self):
        return self.cable_object.id

    @property
    def cable_type(self):
        if 'cable_type' in self.info:
            return self.info['cable_type']
        else:
            return None
    
    @property
    def device_a(self):
        if 'device_a' in self.info:
            return self.info['device_a']
        else:
            return None

    @property
    def device_b(self):
        if 'device_b' in self.info:
            return self.info['device_b']
        else:
            return None

    @property
    def length(self):
        if 'length' in self.info:
            return self.info['length']
        else:
            return None

    @property
    def length_unit(self):
        if 'length_unit' in self.info:
            return self.info['length_unit']
        else:
            return None

    @property
    def port_a(self):
        if 'port_a' in self.info:
            return self.info['port_a']
        else:
            return None

    @property
    def port_b(self):
        if 'port_b' in self.info:
            return self.info['port_b']
        else:
            return None

    @property
    def port_a_type(self):
        if 'port_a_type' in self.info:
            return self.info['port_a_type']
        else:
            return None

    @property
    def port_b_type(self):
        if 'port_b_type' in self.info:
            return self.info['port_b_type']
        else:
            return None

    @property
    def status(self):
        if 'status' in self.info:
            return self.info['status']
        else:
            return None

    @property
    def tags(self):
        if 'tags' in self.info:
            tag_list = list()
            for tag in self.info['tags']:
                tag_list.append(tag_id(self.nb, tag))
            return tag_list
        else:
            return None
