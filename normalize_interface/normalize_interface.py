#! /usr/bin/env python
'''
>>> from normalize_interface import normalize_interface
>>> normalize_interface('fa1/0/35', 'cisco')
'FastEthernet1/0/35'
>>> normalize_interface('fa1/0/35', 'cisco', True)
'Fa1/0/35'
>>> normalize_interface('fast 1/0/35', 'cisco')
'FastEthernet1/0/35'
>>>
'''

from ansible import errors

data_map = {
  "all_interfaces": {
    "Ethernet": [
      "Ethernet",
      "Eth",
      "Et"
    ],
    "Ethernet_reverse": "Et",
    "FastEthernet": [
      "FastEthernet",
      "FastEth",
      "Fas",
      "FE",
      "Fa"
    ],
    "FastEthernet_reverse": "Fa",
    "Management": [
      "Management",
      "Mgmt",
      "Ma"
    ],
    "Management_reverse": "Ma",
    "Tunnel": [
      "Tunnel",
      "Tun",
      "Tu"
    ],
    "Tunnel_reverse": "Tu",
    "GigabitEthernet": [
      "GigabitEthernet",
      "GigEthernet",
      "GigE",
      "Gig",
      "GigEth",
      "GE",
      "Gi"
    ],
    "GigabitEthernet_reverse": "Gi",
    "TenGigabitEthernet": [
      "TenGigabitEthernet",
      "TenGigEthernet",
      "TenGigEth",
      "TenGigE",
      "TenGig",
      "T",
      "Xe"
      "Te"
    ],
    "TenGigabitEthernet_reverse": "Te",
    "FortyGigabitEthernet": [
      "FortyGigabitEthernet",
      "FortyGigEthernet",
      "FortyGigEth",
      "FortyGigE",
      "FortyGig",
      "FGE"
      "Fo"
    ],
    "FortyGigabitEthernet_reverse": "Fo",
    "HundredGigabitEthernet": [
      "HundredGigabitEthernet",
      "HundredGigEthernet",
      "HundredGigEth",
      "HundredGigE",
      "Hu"
    ],
    "HundredGigabitEthernet_reverse": "Hu",
    "Serial": [
      "Serial",
      "Se",
      "S"
    ],
    "Serial_reverse": "Se",
    "VLAN": [
      "VLAN",
      "V",
      "Vl"
    ],
    "VLAN_reverse": "Vl",
    "Multilink": [
      "Multilink",
      "Mu"
    ],
    "Multilink_reverse": "Mu",
    "MFR": [
      "MFR"
    ],
    "MFR_reverse": "MFR",
    "PortChannel": [
      "PortChannel",
      "Port-Channel",
      "Po"
    ],
    "PortChannel_reverse": "Po",
    "POS": [
      "POS",
      "PO"
    ],
    "POS_reverse": "PO",
    "Loopback": [
      "Loopback",
      "Lo"
    ],
    "Loopback_reverse": "Lo",
    "Fddi": [
      "Fddi",
      "FD"
    ],
    "Fddi_reverse": "FD",
    "Virtual-Access": [
      "Virtual-Access",
      "Vi"
    ],
    "Virtual-Access_reverse": "Vi",
    "Virtual-Template": [
      "Virtual-Template",
      "Vt"
    ],
    "Virtual-Template_reverse": "Vt",
    "EOBC": [
      "EOBC",
      "EO"
    ],
    "EOBC_reverse": "EO",
    "ATM": [
      "ATM",
      "AT"
    ],
    "ATM_reverse": "At"
  },
  "dev_os": {
    "eos": {
      "Ethernet": [
        "Ethernet",
        "Ether",
        "Eth",
        "Et"
      ],
      "Ethernet_reverse": "Et"
    },
    "cisco": {
      "FastEthernet": [
        "FastEthernet",
        "FastEth",
        "FastE",
        "Fast",
        "Fas",
        "FE",
        "Fa"
      ],
      "FastEthernet_reverse": "Fa"
    }
  }
}

def _split_base_name(split_interface):
    '''
    simple fuction to split on first digit, slash,  or space match
    '''
    head = split_interface.rstrip(r'/\0123456789 ')
    tail = split_interface[len(head):].lstrip()
    return head, tail

def normalize_interface(interface, device_os, short=False):
    '''
    Function takes in a raw interface and returns a standard interface name.
    e.g. "Fa 1/0" returns as "FastEthernet1/0". The default bucket should work
    in most cases, but can break out OS specific. Additionally can return the
    short name if desired. e.g. "FastEthernet1/1" returns as Fa1/1.
    
    Based on harmonizeInts from cpan Net::Telnet::Cisco::IOS package
    '''

    all_interfaces = data_map['all_interfaces']

    strip_interface = _split_base_name(interface)
    interface_type = strip_interface[0]
    interface_number = strip_interface[1]

    # if the device_os is defined, check if interface is defined, if so, over write
    # this list in all_interfaces
    if device_os in data_map['device_os']:
        for key, value in all_interfaces.items():
            if key in data_map['device_os'][device_os]:
                all_interfaces[key] = data_map['device_os'][device_os][key]

    # go through dictionary and each list within value pair,
    # if match, pull out either long or short form
    for key, value in all_interfaces.items():
        for current_interface in value:
            if current_interface.lower() == interface_type.lower():
                if short:
                    return all_interfaces[key + '_short'] + str(interface_number)
                else:
                    return key + str(interface_number)
    # if nothing matched, at least return the original'
    return interface



class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        return {
            'normalize_interface': normalize_interface
        }
