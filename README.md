<seotitle>netbox-tools: Tools for Netbox operations</seotitle>

# netbox-tools

## News

Recent news about changes that may affect you.

1. 2022-09-29 BREAKING CHANGE: The devices data structure has changed.  Specifically, the ``name`` key was changed to ``device`` and the ``mgmt_interface`` key was changed to ``interface``.  We've added code to ``lib/device.py``, ``lib/interface.py``, ``lib/ip_address.py`` that modifies these keys to the new names, and prints a deprecation warning for each.  To avoid these warnings, update your YAML file(s).  We've modified script args for a few scripts to use the new key names: ``device_create_update.py``, ``device_create_with_ip.py``, ``interface_create_update.py``.

## Getting started

This repo contains python classes and scripts that implement CRUD operations on Netbox using the excellent [pynetbox](https://github.com/netbox-community/pynetbox) library.

Below, you'll find a quick-start setup guide and listing of all the scripts and what they do.

## To clone this repo

```bash
git clone https://github.com/allenrobel/netbox-tools.git
```

## Dependencies

### pynetbox

Install with:

```bash
pip install pynetbox
```

### Ansible (we use ansible vault to store secrets)

Install with:

```bash
pip install ansible
```

### Quick setup guide

netbox-tools uses a python script (netbox_config.py) to load a config file (config.yml) that currently just points your ansible vault file so that the various scripts in this repo have a standard way of finding and reading this file.

1. Edit ./lib/config/netbox_config.py

In this file, edit the line that starts with ``config_file`` and change config_file to point to config.yml (it's also located in lib/config, but you can move it somewhere else if you'd like):

```python
# EDIT THIS LINE TO POINT TO YOUR CONFIG FILE
config_file = '/home/myaccount/netbox-tools/lib/config/config.yml'
```

2. Edit ./lib/config/config.yml

Among other things, config.yml points to your Ansible vault with the line below (in this case, it points to an Ansible vault file named ``secrets``).  Edit this to point to your Ansible vault file.  If you don't have a vault file, we're going to create one in the next step.  There are a couple other options in this file related to SSL certificates which we don't cover here, but which are described in the comments in this file.  If you encounter any urllib3 errors related to SSL certificates, have a look here and play with these options.

```yaml
vault: '/home/myaccount/netbox-tools/lib/config/secrets'
```

3. Create an Ansible vault file.

It is recommended (but not mandatory) that you encrypt your netbox token and url.  The Ansible vault file can contain both of these in plaintext or as encrypted strings.

If you don't care about security, then the file need only contain, e.g.:

```yaml
token: mytoken
url: https://mynetbox.foo.com
```

Where:

- ``mytoken`` comes from your Netbox installation.  In netbox, go to the upper-right corner where there's a dropdown menu that usually says ``Admin`` but may contain your netbox username if you're logged in as someone other than Admin.  Click that, and select ``API Tokens``.  Select one of the tokens on this screen, and paste it into the ``token`` field.

- ``url`` is the base url of your netbox installation, including the port number, if you're using a port other than 80 or 443.  E.g.:

```yaml
url: https://mynetbox.foo.com:8000
```

If you care about security, then you'll want to encrypt these.  As follows (replacing ``/home/myaccount/netbox-tools/lib/config/secrets``, with the location you specified in step 2 above)

```bash
ansible-vault encrypt_string 'mytoken' --name 'token' >> /home/myaccount/netbox-tools/lib/config/secrets
ansible-vault encrypt_string 'myurl' --name 'url' >> /home/myaccount/netbox-tools/lib/config/secrets
```

If you encrypt these items, then ansible-vault will prompt you for a vault password.  You'll use this password later when you run each of the scripts in this repo.

Example:

```bash
% ansible-vault encrypt_string '0123456789abcdef0123456789abcdef11133333' --name 'token' >> /home/myaccount/netbox-tools/lib/config/secrets
New Vault password: 
Confirm New Vault password: 
% ansible-vault encrypt_string 'https://mynetbox.foo.com:8080' --name 'url' >> /home/myaccount/netbox-tools/lib/config/secrets
New Vault password: 
Confirm New Vault password: 
% cat /home/myaccount/netbox-tools/lib/config/secrets
token: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          62653864393663336334643664356430633961633534396262353136643039363761323831393965
          6536353038326234656639646332363266356532326663660a333865323331633237393230646538
          34313266363631346263663331323065386539343661363637626464346563336437363539393361
          3738363662333638310a633163396266613836376135356236663132343737333465386632343938
          36333332323465346434346235393766643630366366316530383238313238396239396239646266
          6634323838313232616263353332356232626439323437313831
url: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          31353832386139656434633734366635646631613839376537643263623139636133356161336632
          6564333230633730363237306564396138383165313834650a623361316337373631613763643531
          35383464636465613361616264663239373262626361626638396661353966393764323739663362
          3239323366376161630a616134353734313466376138333365383131303831626531373764323231
          62656663613739356362386530376330313663343030373165366461626165373232
```

4. Copy netbox-tools/example.yml and edit it to include the information about your equipment.

There are example entries for sites, racks, locations, manufacturers, device types, devices, device roles, and tags.

Follow the comments in this file and create your first device.  Then use the script below to add it to netbox (it adds all the other items as well):

./device_create_all.py --yaml /path/to/your/edited.yml

If you encrypted your token and url, you'll be asked for the ansible vault password you created in step 3 above.

We'll be adding additional things like console ports, etc, as we update this repo.


#### Now you can try

```bash
cd /top/level/directory/for/this/repo
ansible-playbook example_ndfc_rest_fabric_switch_create_f1.yml --ask-vault-pass -i inventory
```

When prompted, enter the password you used in response to the ansible-vault command in step 1 above.

Example:

```bash
% ./device_create_all.py --yaml ./info.yml
Vault password: 
---
Site.update: mysite
---
Location.update: row-a
Location.update: row-b
Location.update: row-c
etc...
```

## Scripts

The first script you should look at is:

Script                        | Description
------------                  | -----------
[device_create_update_all.py] | Creates all sites, locations, manufacturers, device types, devices, device roles, and tags.  Pretty much the main script to get started. 

Below is a complete list. (TODO add the other scripts...)

Script                         | Description
------------                   | -----------
[device_create__update_all.py] | Creates all sites, locations, manufacturers, device types, devices, device roles, and tags.  Pretty much the main script to get started. 


[device_create_update_all.py]: https://github.com/allenrobel/netbox-tools/blob/master/device_create_update_all.py

### Code of Conduct

This repository follows the Contributor Covenant [Code of Conduct](https://github.com/allenrobel/netbox-tools/blob/master/CODE_OF_CONDUCT.md). Please read and familiarize yourself with this document.

### Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) for full text.
