'''
Name: interface.py
Description: Create, update, delete operations on netbox interfaces
'''

from netbox_tools.common import device_id, netbox_id_untagged_vlan

class Interface(object):
    def __init__(self, nb, info):
        self.version = 102
        self.nb = nb
        self.info = info
        self.args = dict()
        self.mandatory_create_update_keys = ['interface', 'device']
        self.mandatory_delete_keys = ['interface', 'device']
        # optional_keys is just FYI.  It's not referenced anywhere.
        self.optional_keys = set()
        self.optional_keys.add('description')
        self.optional_keys.add('duplex')              # str - half, full, auto
        self.optional_keys.add('interface_enabled')   # bool - is the interface enabled
        self.optional_keys.add('interface_mode')      # str - access, tagged, tagged-all
        self.optional_keys.add('interface_type')      # str - interface PHY type
        self.optional_keys.add('label')               # str - physical label
        self.optional_keys.add('mac_address')         # str - interface mac address
        self.optional_keys.add('mgmt_only')           # bool - is the interface only used for management
        self.optional_keys.add('mtu')
        self.optional_keys.add('untagged_vlan')
        self.default_interface_type = '1000base-t'
        self.default_interface_mode = 'access'
        self.default_interface_enabled = True
        self.default_mgmt_only = False
        self.fix_deprecations()

        self.valid_duplex = set()
        self.valid_duplex.add('auto')
        self.valid_duplex.add('full')
        self.valid_duplex.add('half')
        self.valid_duplex = frozenset(self.valid_duplex)

        self.valid_interface_mode = set()
        self.valid_interface_mode.add('access')
        self.valid_interface_mode.add('tagged')
        self.valid_interface_mode.add('tagged-all')
        self.valid_interface_mode = frozenset(self.valid_interface_mode)

        self.valid_interface_type = set()
        self.valid_interface_type.add('1gfc-sfp')
        self.valid_interface_type.add('2gfc-sfp')
        self.valid_interface_type.add('4gfc-sfp')
        self.valid_interface_type.add('8gfc-sfpp')
        self.valid_interface_type.add('16gfc-sfpp')
        self.valid_interface_type.add('32gfc-sfp28')
        self.valid_interface_type.add('64gfc-qsfpp')
        self.valid_interface_type.add('128gfc-qsfp28')
        self.valid_interface_type.add('100base-tx')
        self.valid_interface_type.add('1000base-t')
        self.valid_interface_type.add('2.5gbase-t')
        self.valid_interface_type.add('5gbase-t')
        self.valid_interface_type.add('1000base-x-gbic')
        self.valid_interface_type.add('1000base-x-sfp')
        self.valid_interface_type.add('10g-epon')
        self.valid_interface_type.add('10gbase-t')
        self.valid_interface_type.add('10gbase-cx4')
        self.valid_interface_type.add('10gbase-x-sfpp')
        self.valid_interface_type.add('10gbase-x-xenpak')
        self.valid_interface_type.add('10gbase-x-x2')
        self.valid_interface_type.add('25gbase-x-sfp28')
        self.valid_interface_type.add('50gbase-x-sfp56')
        self.valid_interface_type.add('40gbase-x-qsfpp')
        self.valid_interface_type.add('50gbase-x-sfp28')
        self.valid_interface_type.add('100gbase-x-cfp')
        self.valid_interface_type.add('100gbase-x-cfp2')
        self.valid_interface_type.add('100gbase-x-cfp4')
        self.valid_interface_type.add('100gbase-x-cpak')
        self.valid_interface_type.add('100gbase-x-qsfp28')
        self.valid_interface_type.add('200gbase-x-cfp2')
        self.valid_interface_type.add('200gbase-x-qsfp56')
        self.valid_interface_type.add('400gbase-x-qsfpdd')
        self.valid_interface_type.add('400gbase-x-osfp')
        self.valid_interface_type.add('bridge')
        self.valid_interface_type.add('cdma')
        self.valid_interface_type.add('cisco-stackwise')
        self.valid_interface_type.add('cisco-stackwise-plus')
        self.valid_interface_type.add('cisco-flexstack')
        self.valid_interface_type.add('cisco-flexstack-plus')
        self.valid_interface_type.add('cisco-stackwise-80')
        self.valid_interface_type.add('cisco-stackwise-160')
        self.valid_interface_type.add('cisco-stackwise-320')
        self.valid_interface_type.add('cisco-stackwise-480')
        self.valid_interface_type.add('docsis')
        self.valid_interface_type.add('e1')
        self.valid_interface_type.add('e3')
        self.valid_interface_type.add('epon')
        self.valid_interface_type.add('extreme-summitstack')
        self.valid_interface_type.add('extreme-summitstack-128')
        self.valid_interface_type.add('extreme-summitstack-256')
        self.valid_interface_type.add('extreme-summitstack-512')
        self.valid_interface_type.add('gpon')
        self.valid_interface_type.add('gsm')
        self.valid_interface_type.add('gbase-x-xf')
        self.valid_interface_type.add('ieee802.11a')
        self.valid_interface_type.add('ieee802.11g')
        self.valid_interface_type.add('ieee802.11n')
        self.valid_interface_type.add('ieee802.11ac')
        self.valid_interface_type.add('ieee802.11ad')
        self.valid_interface_type.add('ieee802.11ax')
        self.valid_interface_type.add('ieee802.11ay')
        self.valid_interface_type.add('ieee802.15.1')
        self.valid_interface_type.add('infiniband-sdr')
        self.valid_interface_type.add('infiniband-ddr')
        self.valid_interface_type.add('infiniband-qdr')
        self.valid_interface_type.add('infiniband-fdr10')
        self.valid_interface_type.add('infiniband-fdr')
        self.valid_interface_type.add('infiniband-edr')
        self.valid_interface_type.add('infiniband-hdr')
        self.valid_interface_type.add('infiniband-ndr')
        self.valid_interface_type.add('infiniband-xdr')
        self.valid_interface_type.add('juniper-vcp')
        self.valid_interface_type.add('lag')
        self.valid_interface_type.add('lte')
        self.valid_interface_type.add('ng-pon2')
        self.valid_interface_type.add('other')
        self.valid_interface_type.add('other-wireless')
        self.valid_interface_type.add('sonet-oc3')
        self.valid_interface_type.add('sonet-oc12')
        self.valid_interface_type.add('sonet-oc48')
        self.valid_interface_type.add('sonet-oc192')
        self.valid_interface_type.add('sonet-oc768')
        self.valid_interface_type.add('sonet-oc1920')
        self.valid_interface_type.add('sonet-oc3840')
        self.valid_interface_type.add('t1')
        self.valid_interface_type.add('t3')
        self.valid_interface_type.add('virtual')
        self.valid_interface_type.add('xdsl')
        self.valid_interface_type.add('xg-pon')
        self.valid_interface_type.add('xgs-pon')
        self.valid_interface_type = frozenset(self.valid_interface_type)

    def fix_deprecations(self):
        if 'mgmt_interface' in self.info:
            print('Interface.fix_deprecations: WARNING: devices: <device>: mgmt_interface in your YAML file is deprecated. Use devices: <device>: interface instead.')
            self.info['interface'] = self.info['mgmt_interface']
        if 'name' in self.info:
            print('Interface.fix_deprecations: WARNING: devices: <device>: name in your YAML file is deprecated. Use devices: <device>: device instead.')
            self.info['device'] = self.info['name']

    def validate_delete_keys(self):
        for key in self.mandatory_delete_keys:
            if key not in self.info:
                print('Interface.validate_delete_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)
    def validate_create_update_keys(self):
        for key in self.mandatory_create_update_keys:
            if key not in self.info:
                print('Interface.validate_create_update_keys: exiting. mandatory key {} not found in info {}'.format(key, self.info))
                exit(1)

    def set_duplex(self):
        if self.duplex == None:
            return
        if self.duplex in self.valid_duplex:
            self.args['duplex'] = self.duplex
        else:
            print('Interface.set_duplex: exiting. Invalid duplex. Got {}. Expected one of {}.'.format(
                self.duplex,
                ','.join(sorted(self.valid_duplex))))
            exit(1)

    def set_interface_enabled(self):
        if isinstance(self.interface_enabled, bool):
            self.args['enabled'] = self.interface_enabled
        elif self.interface_enabled == None:
            self.args['enabled'] = self.default_interface_enabled
        else:
            print('Interface.set_interface_enabled: exiting. Invalid value for interface_enabled. Got {}. Expected boolean.'.format(
                self.interface_enabled))
            exit(1)

    def set_interface_mode(self):
        if self.interface_mode == None:
            return
        if self.interface_mode in self.valid_interface_mode:
            self.args['mode'] = self.interface_mode
        else:
            print('Interface.set_interface_mode: exiting. Invalid interface_mode. Got {}. Expected one of {}.'.format(
                self.interface_mode,
                ','.join(sorted(self.valid_interface_mode))))
            exit(1)

    def set_interface_type(self):
        if self.interface_type == None:
            print('Interface.set_interface_type: exiting. missing required argument: interface_type')
            exit(1)
        if self.interface_type in self.valid_interface_type:
            self.args['type'] = self.interface_type
        else:
            print('Interface.set_interface_type: exiting. Invalid interface_type. Got {}. Expected one of {}.'.format(
                self.valid_interface_type,
                ','.join(sorted(self.valid_interface_type))))
            exit(1)

    def set_mgmt_only(self):
        if isinstance(self.mgmt_only, bool):
            self.args['mgmt_only'] = self.mgmt_only
        elif self.mgmt_only == None:
            self.args['mgmt_only'] = self.default_mgmt_only
        else:
            print('Interface.set_mgmt_only: exiting. Invalid value for mgmt_only. Got {}. Expected boolean.'.format(
                self.mgmt_only))
            exit(1)

    def generate_create_update_args(self):
        self.args['name'] = self.interface
        self.args['device'] = device_id(self.nb, self.device)
        if self.args['device'] == None:
            print('Interface.generate_create_update_args: exiting. Device {} does not exist in netbox'.format(self.device))
            exit(1)
        if self.description != None:
            self.args['description'] = self.description
        self.set_duplex()
        self.set_interface_enabled()
        self.set_interface_mode()
        self.set_interface_type()
        self.set_mgmt_only()
        if self.label != None:
            self.args['label'] = self.label
        if self.mac_address != None:
            self.args['mac_address'] = self.mac_address
        if self.mtu != None:
            self.args['mtu'] = self.mtu
        if self.untagged_vlan != None:
            self.args['untagged_vlan'] = netbox_id_untagged_vlan(self.nb, self.untagged_vlan)

    def delete(self):
        print('Interface.delete: {}'.format(self.interface))
        self.validate_delete_keys()
        if self.interface_object == None:
            print('Interface.delete: Nothing to do, interface {} does not exist in netbox.'.format(self.interface))
            return
        try:
            self.interface_object.delete()
        except Exception as e:
            print('Interface.delete: Exiting. Unable to delete interface {}.  Error was: {}'.format(self.interface, e))
            exit(1)

    def create(self):
        print('Interface.create: {} {}'.format(self.device, self.interface))
        try:
            self.nb.dcim.interfaces.create(self.args)
        except Exception as e:
            print('Interface.create: exiting. Unable to create interface {}.  Error was: {}'.format(self.interface, e))
            exit(1)

    def update(self):
        print('Interface.update: {} {}'.format(self.device, self.interface))
        self.args['id'] = self.interface_id
        try:
            self.interface_object.update(self.args)
        except Exception as e:
            print('Interface.update: Exiting. Unable to update interface {}.  Error was: {}'.format(self.interface, e))
            exit(1)

    def create_or_update(self):
        self.validate_create_update_keys()
        self.generate_create_update_args()
        if self.interface_object == None:
            self.create()
        else:
            self.update()

    @property
    def description(self):
        if 'description' in self.info:
            return self.info['description']
        else:
            return None

    @property
    def device(self):
        if 'device' in self.info:
            return self.info['device']
        else:
            print('Interface.device: exiting. Missing required parameter [device].')
            exit(1)

    @property
    def duplex(self):
        if 'duplex' in self.info:
            return self.info['duplex']
        else:
            return None

    @property
    def interface(self):
        if 'interface' in self.info:
            return self.info['interface']
        else:
            print('Interface.interface: exiting. Missing required parameter [interface].')
            exit(1)

    @property
    def interface_object(self):
        return self.nb.dcim.interfaces.get(
            device=self.device,
            name=self.interface)

    @property
    def interface_enabled(self):
        if 'interface_enabled' in self.info:
            return self.info['interface_enabled']
        else:
            return None

    @property
    def interface_id(self):
        return self.interface_object.id

    @property
    def interface_mode(self):
        if 'interface_mode' in self.info:
            return self.info['interface_mode']
        else:
            return None

    @property
    def interface_type(self):
        if 'interface_type' in self.info:
            return self.info['interface_type']
        else:
            return None

    @property
    def label(self):
        if 'label' in self.info:
            return self.info['label']
        else:
            return None

    @property
    def mac_address(self):
        if 'mac_address' in self.info:
            return self.info['mac_address']
        else:
            return None

    @property
    def mgmt_only(self):
        if 'mgmt_only' in self.info:
            return self.info['mgmt_only']
        else:
            return None

    @property
    def mtu(self):
        if 'mtu' in self.info:
            return self.info['mtu']
        else:
            return None

    @property
    def untagged_vlan(self):
        if 'untagged_vlan' in self.info:
            return self.info['untagged_vlan']
        else:
            return None
