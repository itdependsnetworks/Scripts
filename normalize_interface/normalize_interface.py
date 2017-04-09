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
      "GigEthernet",
      "GigE",
      "GigEth",
      "GE",
      "Gi"
    ],
    "GigabitEthernet_reverse": "Gi",
    "TenGigabitEthernet": [
      "TenGigabitEthernet",
      "TenGigEthernet",
      "TenGigEth",
      "T",
      "Te"
    ],
    "TenGigabitEthernet_reverse": "Te",
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
        "Fast",
        "Fas",
        "FE",
        "Fa"
      ],
      "FastEthernet_reverse": "Fa"
    }
  }
}

def split_on_match(split_interface):
    '''
    simple fuction to split on first digit, slash,  or space match
    '''
    head = split_interface.rstrip(r'/\0123456789 ')
    tail = split_interface[len(head):].lstrip()
    return head, tail

def normalize_interface(interface, dev_os, reverse=False):
    '''
    fuction to retun interface normalize
    '''

    all_interfaces = data_map['all_interfaces']
    dev_os_yml = data_map['dev_os']

    strip_interface = split_on_match(interface)
    interface_type = strip_interface[0]
    interface_number = strip_interface[1]

    # if the dev_os is defined, check if interface is defined, if so, over write
    # this list in all_interfaces
    if dev_os in dev_os_yml:
        for key, value in all_interfaces.items():
            if key in dev_os_yml[dev_os]:
                all_interfaces[key] = dev_os_yml[dev_os][key]

    # go through dictionary and each list within value pair,
    # if match, pull out either long or short form
    for key, value in all_interfaces.items():
        for current_interface in value:
            if current_interface.lower() == interface_type.lower():
                if reverse:
                    return all_interfaces[key + '_reverse'] + str(interface_number)
                else:
                    return all_interfaces[key][0] + str(interface_number)
    # if nothing matched, at least return the original'
    return interface



class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        return {
            'normalize_interface': normalize_interface
        }
