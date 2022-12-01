"""
common functions used in netbox-tools
"""
import re
from string import punctuation
import sys
import yaml
import requests
import urllib3
import pynetbox
from netbox_tools.config.netbox_config import LoadConfig
from netbox_tools.credentials import NetboxCredentials


def netbox():
    """
    return a configured netbox instance
    """
    cfg = LoadConfig()
    credentials = NetboxCredentials()
    netbox_instance = pynetbox.api(credentials.url, token=credentials.token)

    session = requests.Session()
    if "ssl_verify" in cfg.config:
        session.verify = cfg.config["ssl_verify"]
    if "disable_insecure_request_warnings" in cfg.config:
        if cfg.config["disable_insecure_request_warnings"] is True:
            # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    netbox_instance.http_session = session
    return netbox_instance


# cable
def cable_id(netbox_instance, label):
    """
    return the netbox cable id, if any, associated with label
    """
    try:
        cable = netbox_instance.dcim.cables.get(label=label)
        if cable is not None:
            return cable.id
        print(
            f"common.cable_id: returning None. cable associated with label {label} does \
            not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.cable_id: returning None for cable label {label}. exception was: {error}"
        )
        return None


# cluster
def cluster_id(netbox_instance, name):
    """
    return the netbox cluster id, if any, associated with name
    """
    try:
        cluster = netbox_instance.virtualization.clusters.get(name=name)
        if cluster is not None:
            return cluster.id
        print(
            f"common.cluster_id: returning None. cluster name {name} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.cluster_id: returning None for cluster {name}. exception was: {error}"
        )
        return None


# cluster_group
def cluster_group_id(netbox_instance, name):
    """
    return the netbox cluster_group id, if any, associated with name
    """
    try:
        cluster_group = netbox_instance.virtualization.cluster_groups.get(name=name)
        if cluster_group is not None:
            return cluster_group.id
        print(
            f"common.cluster_group_id: returning None. cluster_group name {name} does not \
            exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.cluster_group_id: returning None for cluster_group name {name}.\
             exception was: {error}"
        )
        return None


# cluster_type
def cluster_type_id(netbox_instance, name):
    """
    return the netbox cluster_type id, if any, associated with name
    """
    try:
        cluster_type = netbox_instance.virtualization.cluster_types.get(name=name)
        if cluster_type is not None:
            return cluster_type.id
        print(
            f"common.cluster_type_id: returning None. \
            cluster_type name {name} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.cluster_type_id: returning None for cluster_type {name}. \
            Exception detail: {error}"
        )
        return None


# console_port
def get_console_ports(netbox_instance):
    """
    return all currently defined netbox console ports
    """
    return netbox_instance.dcim.console_ports.all()


def get_console_port(netbox_instance, device, port):
    """
    Given netbox instance, device name, and port, return console_port object.
    If console_port does not exist in netbox, return None
    """
    try:
        console_port = netbox_instance.dcim.console_ports.get(device=device, name=port)
        if console_port is not None:
            return console_port
        print(
            f"common.console_port: returning None. \
            console_port device {device} port {port} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(f"common.console_port: returning None. exception was: {error}")
        return None


def console_port_id(netbox_instance, device, port):
    """
    Given netbox instance, device name, and port, return console_port ID.
    If console_port does not exist in netbox, return None
    """
    try:
        console_port = netbox_instance.dcim.console_ports.get(device=device, name=port)
        if console_port is not None:
            return console_port.id
        print(
            f"common.console_port_id: returning None. \
            console_port device {device} port {port} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.console_port_id: \
            returning None for device {device} console_port {port}. \
            Exception detail: {error}"
        )
        return None


# console_server_port
def get_console_server_ports(netbox_instance):
    """
    Given netbox instance, return all currently-defined console_server_ports
    """
    return netbox_instance.dcim.console_server_ports.all()


def get_console_server_port(netbox_instance, device, port):
    """
    Given netbox instance, device name, and port, return console_server_port object.
    If console_server_port does not exist in netbox, return None
    """
    try:
        console_server_port = netbox_instance.dcim.console_server_ports.get(
            device=device, name=port
        )
        if console_server_port is not None:
            return console_server_port
        print(
            f"common.console_server_port: returning None. \
            console_server_port device {device} port {port} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(f"common.console_server_port: returning None. exception was: {error}")
        return None


def console_server_port_id(netbox_instance, device, port):
    """
    Given netbox instance, device name, and port, return console_server_port ID.
    If console_server_port does not exist in netbox, return None
    """
    try:
        console_server_port = netbox_instance.dcim.console_server_ports.get(
            device=device, name=port
        )
        if console_server_port is not None:
            return console_server_port.id
        print(
            f"common.console_server_port: returning None. \
            console_server_port device {device} port {port} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.console_server_port: \
            returning None for device {device} console_server_port {port}. \
            Exception detail: {error}"
        )
        return None


# device
def get_device(netbox_instance, name):
    """
    Given netbox instance and device name, return device.
    If device does not exist in netbox, return None
    """
    try:
        device = netbox_instance.dcim.devices.get(name=name)
        if device is not None:
            return device
        print(f"common.device: returning None. device {name} does not exist in netbox")
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.device: returning None for device name {name}. exception was: {error}"
        )
        return None


def device_id(netbox_instance, name):
    """
    Given netbox instance and device name, return device_id.
    If device does not exist in netbox, return None
    """
    try:
        device = netbox_instance.dcim.devices.get(name=name)
        if device is not None:
            return device.id
        print(
            f"common.device_id: returning None. device {name} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.device_id: returning None for device name {name}. exception was: {error}"
        )
        return None


# device_type
def get_device_type(netbox_instance, name):
    """
    Given netbox instance and device_type name, return device_type.
    If device_type does not exist in netbox, return None
    """
    try:
        device_type = netbox_instance.dcim.device_types.get(slug=name.lower())
        return device_type
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.get_device_type: returning None for device_type {name}. exception was: {error}"
        )
        return None


def device_type_id(netbox_instance, name):
    """
    Given netbox instance and device_type name, return device_type_id.
    If device_type does not exist in netbox, return None
    """
    try:
        device_type = netbox_instance.dcim.device_types.get(model=name)
        if device_type is not None:
            return device_type.id
        print(
            f"common.device_type_id: returning None. device_type {name} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.device_type_id: returning None for device_type {name}. \
            Exception detail: {error}"
        )
        return None


# interface
def get_interface(netbox_instance, device, interface):
    """
    Given netbox instance, device name, interface name, return interface object
    If interface does not exist in netbox, return None
    """
    try:
        interface_object = netbox_instance.dcim.interfaces.get(
            name=interface, device=device
        )
        return interface_object
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.get_interface: returning None for device {device} interface {interface}. \
            Exception detail: {error}"
        )
        return None


def interface_id(netbox_instance, device, interface):
    """
    Given netbox instance, device name, interface name, return interface id
    If interface does not exist in netbox, return None
    """
    try:
        interface_object = netbox_instance.dcim.interfaces.get(
            name=interface, device=device
        )
        if interface_object is not None:
            return interface_object.id
        print(
            f"common.interface_id: returning None. device {device} interface {interface} \
            does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.interface_id: returning None for device {device} interface {interface}. \
            Exception detail: {error}"
        )
        return None


# ip address
def get_ip_address(netbox_instance, ip4):
    """
    Given netbox instance, and ip address with format A.B.C.D/E, return netbox ip address object.
    If address doesn't exist within netbox, return None
    """
    try:
        address, mask = ip4.split("/")
    except (ValueError, Exception) as error:
        print(
            f"exiting. Unexpected format for prefix. Expected A.B.C.D/E, got {ip4}. \
            Exception detail: {error}"
        )
        sys.exit(1)
    try:
        return netbox_instance.ipam.ip_addresses.get(address=address, mask=mask)
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.get_ip_address: returning None for ip {ip4}. \
            Exception detail: {error}"
        )
        return None

def make_ip_address_dict(ip_addresses_dict, interface_dict):
    """
    Return a dictionary with the keys expected by the IpAddress class.

    Parameters:
       ip_addresses_dict: the entire ip4_addresses dict, see example.yml in this repo
       interface_dict: dictionary for one interface culled from the interfaces dict in example.yml
    """
    if 'ip4' not in interface_dict:
        return None
    ip_address_dict = {}
    if 'device' in interface_dict:
        device_key = 'device'
    elif 'virtual_machine' in interface_dict:
        device_key = 'virtual_machine'
    else:
        print("common.make_ip_address_dict: exiting")
        print("interface_dict missing key: 'device' or 'virtual_machine'")
        sys.exit(1)
    ip4 = interface_dict['ip4']
    try:
        ip_address_dict = {}
        ip_address_dict['ip4'] = ip4
        ip_address_dict['interface'] = interface_dict['interface']
        ip_address_dict[device_key] = interface_dict[device_key]
    except KeyError as _key_error_exception:
        print(f"missing mandatory key in interface_dict {interface_dict}")
        print("mandatory keys: ip4, interface, [device or virtual_machine]")
        print(f"Exception detail: {_key_error_exception}")
        sys.exit(1)
    if ip4 not in ip_addresses_dict:
        return ip_address_dict
    if 'description' in ip_addresses_dict[ip4]:
        ip_address_dict['description'] = ip_addresses_dict[ip4]['description']
    else:
        ip_address_dict['description'] = ""
    if 'role' in ip_addresses_dict[ip4]:
        ip_address_dict['role'] = ip_addresses_dict[ip4]['role']
    else:
        ip_address_dict['role'] = ""
    if 'status' in ip_addresses_dict[ip4]:
        ip_address_dict['status'] = ip_addresses_dict[ip4]['status']
    else:
        ip_address_dict['status'] = ""
    if 'tags' in ip_addresses_dict[ip4]:
        ip_address_dict['tags'] = ip_addresses_dict[ip4]['tags']
    else:
        ip_address_dict['tags'] = []
    return ip_address_dict


def ip_address_id(netbox_instance, ip4):
    """
    Given netbox instance, and ip address with format A.B.C.D/E, return netbox ip address id.
    If ip address doesn't exist within netbox, return None
    """
    try:
        address, mask = ip4.split("/")
    except (ValueError, Exception) as error:
        print(
            f"exiting. Unexpected format for prefix. Expected A.B.C.D/E, got {ip4}. \
            Exception detail: {error}"
        )
        sys.exit(1)
    try:
        ip_address = netbox_instance.ipam.ip_addresses.get(address=address, mask=mask)
        if ip_address is not None:
            return ip_address.id
        print(
            f"common.ip_address_id: returning None. ipv4 address {ip4} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.ip_address_id: returning None for ip {ip4}. exception was: {error}"
        )
        return None


# virtualization/interfaces virtual_interface
def get_virtual_interface(netbox_instance, virtual_machine, virtual_interface):
    """
    Given netbox instance, virtual_machine name, virtual_interface name,
    return virtual_interface object

    If virtual_interface does not exist in netbox, return None
    """
    try:
        virtual_interface_object = netbox_instance.virtualization.interfaces.get(
            name=virtual_interface, virtual_machine=virtual_machine
        )
        return virtual_interface_object
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.get_virtual_interface: returning None for virtual_machine {virtual_machine} \
            virtual_interface {virtual_interface}. exception was: {error}"
        )
        return None


def virtual_interface_id(netbox_instance, virtual_machine, virtual_interface):
    """
    Given netbox instance, virtual_machine name, virtual_interface name, return virtual_interface id
    If virtual_interface does not exist in netbox, return None
    """
    try:
        virtual_interface_object = netbox_instance.virtualization.interfaces.get(
            name=virtual_interface, virtual_machine=virtual_machine
        )
        if virtual_interface_object is not None:
            return virtual_interface_object.id
        print(
            f"common.ip_address_id: returning None. virtual_machine {virtual_machine} \
            virtual_interface {virtual_interface} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.virtual_interface_id: returning None for virtual_machine {virtual_machine} \
            virtual_interface {virtual_interface}. exception was: {error}"
        )
        return None


# vlans
def netbox_id_untagged_vlan(netbox_instance, vid):
    """
    Given netbox instance and vid (vlan id), return netbox id for vlan.
    If vlan does not exist in netbox, return None
    """
    try:
        vlan_object = netbox_instance.ipam.vlans.get(vid=vid)
        if vlan_object is not None:
            return vlan_object.id
        print(
            f"common.netbox_id_untagged_vlan: returning None. vid {vid} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.netbox_id_untagged_vlan: returning None for vid {vid}. exception was: {error}"
        )
        print(
            f"common.netbox_id_untagged_vlan: possibly vlan ID (vid) {vid} does not yet exist in \
            netbox, in which case you need to create it first."
        )
        return None


def vlan_name_to_id(netbox_instance, vlan_name):
    """
    Given netbox instance and Vlan name, return Netbox id.
    If vlan does not exist in netbox, return None
    """
    try:
        vlan_object = netbox_instance.ipam.vlans.get(name=vlan_name)
        if vlan_object is not None:
            return vlan_object.id
        print(
            f"common.vlan_name_to_id: returning None. vlan_name {vlan_name} \
            does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.vlan_name_to_id: returning None for vlan_name {vlan_name}. \
            exception was: {error}"
        )
        print(
            f"common.vlan_name_to_id: possibly vlan_name {vlan_name} does not yet exist in netbox, \
            in which case you need to create it first."
        )
        return None


def vlan_vid_to_id(netbox_instance, vlan_vid):
    """
    Given netbox instance and Vlan vid, return Netbox id.
    If vlan does not exist in netbox, return None
    """
    try:
        vlan_object = netbox_instance.ipam.vlans.get(vid=vlan_vid)
        if vlan_object is not None:
            return vlan_object.id
        print(
            f"common.vlan_vid_to_id: returning None. vlan_vid {vlan_vid} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.vlan_vid_to_id: returning None for vlan_vid {vlan_vid}. exception was: {error}"
        )
        print(
            f"common.vlan_vid_to_id: possibly vlan_vid {vlan_vid} does not yet exist in netbox, \
            in which case you need to create it first."
        )
        return None


def vlan_group_id(netbox_instance, vlan_group_name):
    """
    Given netbox instance and VlanGroup name, return vlan_group_id.
    If vlan_group does not exist in netbox, return None
    """
    try:
        vlan_group_object = netbox_instance.ipam.vlan_groups.get(name=vlan_group_name)
        if vlan_group_object is not None:
            return vlan_group_object.id
        print(
            f"common.vlan_group_id: returning None. vlan_group_name {vlan_group_name} \
            does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.vlan_group_id: returning None for vlan_group_name {vlan_group_name}. \
            exception was: {error}"
        )
        return None


# location
def location_id(netbox_instance, name):
    """
    Given netbox instance and location name, return location id.
    If location doesn't exist within netbox, return None
    """
    try:
        location = netbox_instance.dcim.locations.get(name=name)
        if location is not None:
            return location.id
        print(
            f"common.location_id: returning None. location name {name} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.location_id: returning None for location {name}. exception was: {error}"
        )
        return None


# rack
def rack_id(netbox_instance, name):
    """
    Given netbox instance and rack name, return rack id.
    If rack doesn't exist within netbox, return None
    """
    try:
        rack = netbox_instance.dcim.racks.get(name=name)
        if rack is not None:
            return rack.id
        print(
            f"common.rack_id: returning None. rack name {name} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(f"common.rack_id: returning None for rack {name}. exception was: {error}")
        return None


# manufacturer
def get_manufacturer(netbox_instance, name):
    """
    Given netbox instance and manufacturer name, return manufacturer.
    If manufacturer doesn't exist within netbox, return None
    """
    try:
        manufacturer = netbox_instance.dcim.manufacturers.get(name=name)
        return manufacturer
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.get_manufacturer: returning None for manufacturer {name}.\
             exception was: {error}"
        )
        return None


def manufacturer_id(netbox_instance, name):
    """
    Given netbox instance and manufacturer name, return manufacturer id.
    If manufacturer doesn't exist within netbox, return None
    """
    try:
        manufacturer = netbox_instance.dcim.manufacturers.get(name=name)
        if manufacturer is not None:
            return manufacturer.id
        print(
            f"common.manufacturer_id: returning None. manufacturer name {name} \
            does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.manufacturer_id: returning None for manufacturer {name}. \
            exception was: {error}"
        )
        return None


# role
def get_role(netbox_instance, name):
    """
    Given netbox instance and device role name, return device role.
    If device role doesn't exist within netbox, return None
    """
    try:
        role = netbox_instance.dcim.device_roles.get(name=name)
        return role
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.get_role: returning None for role {name}. exception was: {error}"
        )
        return None


def role_id(netbox_instance, name):
    """
    Given netbox instance and role name, return role id.
    If device role doesn't exist within netbox, return None
    """
    try:
        role = netbox_instance.dcim.device_roles.get(name=name)
        if role is not None:
            return role.id
        print(
            f"common.role_id: returning None. role name {name} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.role_id: returning None for role_id associated with role {name}. \
            exception was: {error}"
        )
        return None


# site
def site_id(netbox_instance, name):
    """
    Given netbox instance and site name, return site id.
    If site doesn't exist within netbox, return None
    """
    try:
        site = netbox_instance.dcim.sites.get(name=name)
        if site is not None:
            return site.id
        print(
            f"common.site_id: returning None. site name {name} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.site_id: returning None for site_id associated with site {name}. \
            exception was: {error}"
        )
        return None


# tag
def get_tag(netbox_instance, name):
    """
    Given netbox instance and tag name, return tag.
    If tag doesn't exist within netbox, return None
    """
    try:
        tag = netbox_instance.extras.tags.get(name=name)
        if tag is None:
            print(
                f"common.get_tag: returning None. tag {name} does not exist in netbox.".format(
                    name
                )
            )
        return tag
    except (pynetbox.RequestError, Exception) as error:
        print(f"common.get_tag: returning None for tag {name}. exception was: {error}")
        return None


def tag_id(netbox_instance, name):
    """
    Given netbox instance and tag name, return tag id.
    If tag doesn't exist within netbox, return None
    """
    try:
        tag = netbox_instance.extras.tags.get(name=name)
        if tag is not None:
            return tag.id
        print(
            f"common.tag_id: returning None. tag name {name} does not exist in netbox"
        )
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(
            f"common.tag_id: returning None for tag_id associated with tag {name}. \
            exception was: {error}"
        )
        return None


def get_tags(netbox_instance):
    """
    Given netbox instance, return all tag names currently configured in netbox.
    """
    try:
        tags = netbox_instance.extras.tags.all()
        return [tag.name for tag in tags]
    except (pynetbox.RequestError, Exception) as error:
        print(f"common.get_tags: returning None. exception was: {error}")
        return None


def get_vm(netbox_instance, name):
    """
    Given netbox instance and vm name, return vm.
    If vm does not exist in netbox, return None
    """
    try:
        vm_obj = netbox_instance.virtualization.virtual_machines.get(name=name)
        if vm_obj is not None:
            return vm_obj
        print(f"common.get_vm: returning None. vm {name} does not exist in netbox")
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(f"common.get_vm: returning None for vm {name}. exception was: {error}")
        return None


def vm_id(netbox_instance, name):
    """
    Given netbox instance and vm name, return vm id.
    If vm doesn't exist within netbox, return None
    """
    try:
        vm_obj = netbox_instance.virtualization.virtual_machines.get(name=name)
        if vm_obj is not None:
            return vm_obj.id
        print(f"common.vm_id: returning None. vm name {name} does not exist in netbox")
        return None
    except (pynetbox.RequestError, Exception) as error:
        print(f"common.vm_id: returning None for vm {name}. exception was: {error}")
        return None


# utility functions
def create_slug(slug):
    """
    Convert str() s into a slug that netbox accepts.
        1. remove all punctuation
        2. replace spaces with '-'
        3. convert to lower-case
    """
    regex = re.compile(r"[{}]+".format(re.escape(punctuation)))
    slug = regex.sub("", slug)
    slug = slug.replace(" ", "-")
    return slug.lower()


def load_yaml(filename):
    """
    load yaml file
    """
    try:
        with open(filename, "r", encoding="utf8") as file_handle:
            contents = yaml.load(file_handle, Loader=yaml.FullLoader)
        return contents
    except Exception as error:
        print(f"common.load_yaml: exiting. Exception was: {error}")
        sys.exit(1)
