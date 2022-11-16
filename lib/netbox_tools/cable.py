'''
Name: cable.py
Description: Class for create, update, and delete operations on netbox cable
'''
from inspect import stack
import sys
from pynetbox import RequestError
from netbox_tools.common import interface_id
from netbox_tools.common import tag_id
from netbox_tools.colors import color_to_rgb
OUR_VERSION = 103

class Cable():
    '''
    create, update, and delete operations on netbox dcim.cable
    '''
    def __init__(self, netbox, info):
        self._netbox = netbox
        self._info = info
        self.lib_version = OUR_VERSION
        self._classname = __class__.__name__
        self._args = {}
        self._populate_optional_keys()
        self._populate_valid_port_types()
        self._populate_port_type_map()
        self._populate_mandatory_keys()
        self._populate_valid_choices()


    def log(self, msg):
        print('{}(v{}).{}: {}'.format(self._classname, self.lib_version, stack()[1].function, msg))


    def _populate_valid_port_types(self):
        self._valid_port_types = set()
        self._valid_port_types.add('interface')
        self._valid_port_types.add('console_server')
        self._valid_port_types.add('console')
        self._valid_port_types.add('power')


    def _populate_port_type_map(self):
        self._port_type_map = {}
        self._port_type_map['interface'] = 'dcim.interface'
        self._port_type_map['console_server'] = 'dcim.console_server_port'
        self._port_type_map['console'] = 'dcim.console_port'
        self._port_type_map['power'] = 'dcim.power_outlet'


    def _populate_optional_keys(self):
        self._optional_keys = set()
        self._optional_keys.add('color') # str - a color from colors.py in this repo, or a hex rgb color value, e.g. for red: f44336
        self._optional_keys.add('length') # int
        self._optional_keys.add('length_unit') # str
        self._optional_keys.add('status') # str
        self._optional_keys.add('tags') # a list of tags to associate with the cable
        self._optional_keys.add('type') # str


    def _populate_mandatory_keys(self):
        self._mandatory_keys_create_or_update = set()
        self._mandatory_keys_create_or_update.add('label') # A UNIQUE label to identify the cable
        self._mandatory_keys_create_or_update.add('device_a') # termination_a device name
        self._mandatory_keys_create_or_update.add('device_b') # termination_b device name
        self._mandatory_keys_create_or_update.add('port_a') # termination_a port name
        self._mandatory_keys_create_or_update.add('port_b') # termination_b port name
        self._mandatory_keys_create_or_update.add('port_a_type') # termination_a port type: interface, console, console_server, power
        self._mandatory_keys_create_or_update.add('port_b_type') # termination_a port type: interface, console, console_server, power
        self._mandatory_keys_delete = set()
        self._mandatory_keys_delete.add('label')


    def _populate_valid_choices(self):
        '''
        pull the valid choices for dcim.cables from Netbox so we can use them
        to validate caller's input, and provide caller a list of valid choices
        of they provide invalid input.
        '''
        self.valid_choices = {}
        choices_dict = self._netbox.dcim.cables.choices()
        for item in choices_dict:
            valid_values = choices_dict[item]
            self.valid_choices[item] = [item['value'] for item in valid_values]


    def _validate_keys_delete(self):
        '''
        ensure the caller has set all keys required by the delete method
        '''
        for key in self._mandatory_keys_delete:
            if key not in self._info:
                self.log('exiting. mandatory key {} not found in info {}'.format(key, self._info))
                sys.exit(1)


    def _validate_keys_create_or_update(self):
        '''
        ensure the caller has set all keys required by the create and update methods
        '''
        for key in self._mandatory_keys_create_or_update:
            if key not in self._info:
                self.log('exiting. mandatory key {} not found in info {}'.format(key, self._info))
                sys.exit(1)


    def _set_cable_type(self):
        '''
        add the caller's cable type, if any
        '''
        if self.cable_type is None:
            return
        if self.cable_type in self.valid_choices['type']:
            self._args['type'] = self.cable_type
        else:
            self.log('exiting. Invalid cable_type. Got {}. Expected one of {}.'.format(
                self.cable_type,
                ','.join(sorted(self.valid_choices['type']))))
            sys.exit(1)


    def _set_color(self):
        '''
        add the caller's cable color, if any
        '''
        if self.rgb is None:
            return
        self._args['color'] = self.rgb

    def _set_label(self):
        '''
        add the caller's cable label
        '''
        self._args['label'] = self.label

    def _set_length(self):
        '''
        add the caller's cable length, if any
        '''
        if self.length is None:
            return
        if isinstance(self.length, int):
            self._args['length'] = self.length
        else:
            self.log('exiting. Expected type int for length. Got {}'.format(self.length))
            sys.exit(1)

    def _set_length_unit(self):
        '''
        add the caller's length_unit, if any
        '''
        if self.length_unit is None:
            return
        if self.length_unit in self.valid_choices['length_unit']:
            self._args['length_unit'] = self.length_unit
        else:
            self.log('exiting. Invalid length_unit. Got {}. Expected one of {}.'.format(
                self.length_unit,
                ','.join(sorted(self.valid_choices['length_unit']))))
            sys.exit(1)

    def _set_status(self):
        '''
        add the caller's cable status, if any
        '''
        if self.status is None:
            return
        if self.status in self.valid_choices['status']:
            self._args['status'] = self.status
        else:
            self.log('exiting. Invalid status. Got {}. Expected one of {}.'.format(
                self.status,
                ','.join(sorted(self.valid_choices['status']))))
            sys.exit(1)

    def _set_a_terminations(self):
        '''
        add the caller's a_terminations, if any
        '''
        if self.device_a is None:
            self.log('exiting. Missing mandatory parameter: device_a')
            sys.exit(1)
        if self.port_a is None:
            self.log('exiting. Missing mandatory parameter: port_a')
            sys.exit(1)
        if self.port_a_type is None:
            self.log('exiting. Missing mandatory parameter: port_a_type')
            sys.exit(1)
        if self.port_a_type not in self._valid_port_types:
            self.log('exiting. Unexpected port_a_type. Got {}. Expected one of {}.'.format(
                self.port_a_type,
                ','.join(self._valid_port_types)))
            sys.exit(1)
        self._args['a_terminations'] = []
        termination = {}
        termination['object_id'] = interface_id(self._netbox, self.device_a, self.port_a)
        termination['object_type'] = self._port_type_map[self.port_a_type]
        self._args['a_terminations'].append(termination)

    def _set_b_terminations(self):
        '''
        add the caller's b_terminations, if any
        '''
        if self.device_b is None:
            self.log('exiting. Missing mandatory parameter: device_b')
            sys.exit(1)
        if self.port_b is None:
            self.log('exiting. Missing mandatory parameter: port_b')
            sys.exit(1)
        if self.port_b_type is None:
            self.log('exiting. Missing mandatory parameter: port_b_type')
            sys.exit(1)
        if self.port_b_type not in self._valid_port_types:
            self.log('exiting. Unexpected port_b_type. Got {}. Expected one of {}.'.format(
                self.port_b_type,
                ','.join(self._valid_port_types)))
            sys.exit(1)
        self._args['b_terminations'] = []
        termination = {}
        termination['object_id'] = interface_id(self._netbox, self.device_b, self.port_b)
        termination['object_type'] = self._port_type_map[self.port_b_type]
        self._args['b_terminations'].append(termination)


    def _set_tags(self):
        '''
        add the caller's tags, if any
        '''
        if self.tags is not None:
            self._args['tags'] = self.tags


    def _generate_args_create_or_update(self):
        '''
        generate all supported arguments
        '''
        self._set_cable_type()
        self._set_color()
        self._set_label()
        self._set_length_unit()
        self._set_status()
        self._set_length()
        self._set_a_terminations()
        self._set_b_terminations()
        self._set_tags()


    def create(self):
        '''
        create a cable
        '''
        self.log('{}'.format(self.label))
        try:
            self._netbox.dcim.cables.create(self._args)
        except RequestError as request_error:
            self.log('exiting. RequestError Unable to create Cable {}.  Error was: {}'.format(self.label, request_error))
            sys.exit(1)
        except Exception as general_error:
            self.log('exiting. Unable to create Cable {}.  Error was: {}'.format(self.label, general_error))
            sys.exit(1)


    def update(self):
        '''
        update a cable

        Note: There's a bug that causes update not to work for cable.

        https://github.com/netbox-community/pynetbox/issues/491

        For now, we delete the cable, then recreate it with the new args.
        This results in the cable_id changing though, which isn't ideal since
        the change log will only ever have one entry, and journel entries will
        be deleted.
        '''
        self.log('Cable.update: {} cable_id {}'.format(self.label, self.cable_id))
        try:
            self.cable_object.delete()
        except RequestError as request_error:
            self.log('exiting. RequestError Unable to delete Cable {}.  Error was: {}'.format(self.label, request_error))
            sys.exit(1)
        except Exception as general_error:
            self.log('Unable to delete cable {} prior to recreate due to {}'.format(self.label, general_error))
            self.log('proceeding nonetheless...')

        try:
            self._netbox.dcim.cables.create(self._args)
        except RequestError as request_error:
            self.log('exiting. RequestError Unable to update Cable {}.  Error was: {}'.format(self.label, request_error))
            sys.exit(1)
        except Exception as general_error:
            self.log('exiting. Unable to update Cable {}.  Error was: {}'.format(self.label, general_error))
            sys.exit(1)

    # def _update(self):
    #     self.log('{} cable_id {}'.format(self.label, self.cable_id))
    #     try:
    #         self.cable_object.update(self._args)
    #     except Exception as general_error:
    #         self.log('Unable to update cable {}. Error was: {}'.format(self.label, general_error))
    #         self.log('args: {}'.format(self._args))
    #         sys.exit(1)

    def delete(self):
        '''
        delete a cable
        '''
        self.log('{}'.format(self.label))
        self._validate_keys_delete()
        if self.cable_object is None:
            self.log('Nothing to do, Cable {} does not exist in netbox.'.format(self.label))
            return
        try:
            self.cable_object.delete()
        except RequestError as request_error:
            self.log('exiting. RequestError Unable to delete Cable {}.  Error was: {}'.format(self.label, request_error))
            sys.exit(1)
        except Exception as general_error:
            self.log('exiting. Unable to delete Cable {}.  Error was: {}'.format(self.label, general_error))
            sys.exit(1)


    def create_or_update(self):
        '''
        entry point into creation and updation methods
        '''
        self._validate_keys_create_or_update()
        self._generate_args_create_or_update()
        if self.cable_object is None:
            self.create()
        else:
            self.update()

    @property
    def color(self):
        '''
        set the cable's netbox color
        '''
        if 'color' in self._info:
            return self._info['color']
        return None

    @property
    def rgb(self):
        '''
        return the rgb value of a supported color name
        '''
        if self.color is None:
            return None
        return color_to_rgb(self._info['color'])

    @property
    def label(self):
        '''
        set a cable's physical label
        '''
        return self._info['label']

    @property
    def cable_object(self):
        '''
        return a cable object by searching for the cable's label
        '''
        return self._netbox.dcim.cables.get(label=self.label)

    @property
    def cable_id(self):
        '''
        return the cable's netbox id set by the caller
        '''
        return self.cable_object.id

    @property
    def cable_type(self):
        '''
        return the cable's type set by the caller
        '''
        if 'cable_type' in self._info:
            return self._info['cable_type']
        return None

    @property
    def device_a(self):
        '''
        return the cable's device_a termination set by the caller
        '''
        if 'device_a' in self._info:
            return self._info['device_a']
        return None

    @property
    def device_b(self):
        '''
        return the cable's device_b termination set by the caller
        '''
        if 'device_b' in self._info:
            return self._info['device_b']
        return None

    @property
    def length(self):
        '''
        return the cable's length set by the caller
        '''
        if 'length' in self._info:
            return self._info['length']
        return None

    @property
    def length_unit(self):
        '''
        return the cable's length unit (e.g. m, km) set by the caller
        '''
        if 'length_unit' in self._info:
            return self._info['length_unit']
        return None

    @property
    def port_a(self):
        '''
        return the cable's port_a termination set by the caller
        '''
        if 'port_a' in self._info:
            return self._info['port_a']
        return None

    @property
    def port_b(self):
        '''
        return the cable's port_b termination set by the caller
        '''
        if 'port_b' in self._info:
            return self._info['port_b']
        return None

    @property
    def port_a_type(self):
        '''
        return the cable's port_a port-type set by the caller
        '''
        if 'port_a_type' in self._info:
            return self._info['port_a_type']
        return None

    @property
    def port_b_type(self):
        '''
        return the cable's port_b port-type set by the caller
        '''
        if 'port_b_type' in self._info:
            return self._info['port_b_type']
        return None

    @property
    def status(self):
        '''
        return the cable's status set by the caller
        '''
        if 'status' in self._info:
            return self._info['status']
        return None

    @property
    def tags(self):
        '''
        return the cable's tags set by the caller
        '''
        if 'tags' in self._info:
            tag_list = []
            for tag in self._info['tags']:
                tag_list.append(tag_id(self._netbox, tag))
            return tag_list
        return None
